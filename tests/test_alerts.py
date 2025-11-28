import unittest
from datetime import datetime, timedelta
from processor import group_and_sort_events, detect_alerts

class TestHeartbeatAlerts(unittest.TestCase):

    def test_working_alert_case(self):
        # This case should produce an alert after 3 consecutive misses
        events = [
            {"service": "svc", "timestamp": "2025-08-04T10:00:00Z"},
            {"service": "svc", "timestamp": "2025-08-04T10:01:00Z"},
            # next recorded heartbeat at 10:05 -> misses at 10:02,10:03,10:04 -> alert at 10:04
            {"service": "svc", "timestamp": "2025-08-04T10:05:00Z"}
        ]
        grouped = group_and_sort_events(events)
        alerts = detect_alerts(grouped, expected_interval_seconds=60, allowed_misses=3)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["service"], "svc")
        self.assertEqual(alerts[0]["alert_at"], "2025-08-04T10:04:00Z")

    def test_near_miss_no_alert(self):
        events = [
            {"service": "x", "timestamp": "2025-08-04T10:00:00Z"},
            {"service": "x", "timestamp": "2025-08-04T10:01:00Z"},
            # next at 10:04 -> misses at 10:02,10:03 => only 2 misses, no alert
            {"service": "x", "timestamp": "2025-08-04T10:04:00Z"}
        ]
        grouped = group_and_sort_events(events)
        alerts = detect_alerts(grouped, expected_interval_seconds=60, allowed_misses=3)
        self.assertEqual(alerts, [])

    def test_unordered_input(self):
        # events out of order should still work
        events = [
            {"service": "a", "timestamp": "2025-08-04T10:05:00Z"},
            {"service": "a", "timestamp": "2025-08-04T10:00:00Z"},
            {"service": "a", "timestamp": "2025-08-04T10:01:00Z"},
        ]
        grouped = group_and_sort_events(events)
        alerts = detect_alerts(grouped, expected_interval_seconds=60, allowed_misses=3)
        # There will be misses at 10:02,10:03,10:04 => alert at 10:04
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["alert_at"], "2025-08-04T10:04:00Z")

    def test_malformed_events_skipped(self):
        events = [
            {"service":"b","timestamp":"2025-08-04T10:00:00Z"},
            {"service":"b"},  # missing timestamp
            {"timestamp":"2025-08-04T10:02:00Z"},  # missing service
            {"service":"b","timestamp":"not-a-timestamp"}  # invalid timestamp
        ]
        grouped = group_and_sort_events(events)
        # Only one valid event -> no alert
        alerts = detect_alerts(grouped, expected_interval_seconds=60, allowed_misses=3)
        self.assertEqual(alerts, [])

    def test_print_alerts_from_file(self):
        # Load the provided events.json dataset
        import json, os
        here = os.path.dirname(__file__)
        path = os.path.join(here, "..", "events.json")
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        grouped = group_and_sort_events(raw)
        alerts = detect_alerts(grouped, expected_interval_seconds=60, allowed_misses=3)
        
        # Print the final alerts JSON
        print("\nAlerts detected from events.json:")
        print(json.dumps(alerts, indent=2))


if __name__ == "__main__":
    unittest.main()
