from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.parser import isoparse  # type: ignore
from typing import List, Dict, Any, Optional


def parse_event(e: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Safely validate and convert a raw event {service, timestamp} into a structured Python object."""
    service = e.get("service") 
    ts = e.get("timestamp")
    if not service or not ts:
        return None
    try:
        dt = isoparse(ts) # To convert ISO-8601 timestamp string into a Python datetime.
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=None)
        return {"service": service, "timestamp": dt}
    except Exception:
        return None


def group_and_sort_events(raw_events: List[Dict[str, Any]]) -> Dict[str, List[datetime]]:
    """Group events by service and sort each service’s events chronologically."""
    grouped = defaultdict(list)
    for e in raw_events:
        parsed = parse_event(e)
        if parsed:
            grouped[parsed["service"]].append(parsed["timestamp"])

    for svc in grouped:
        grouped[svc].sort() # sorts timestamps from earliest → latest (in ascending order)

    return grouped


def detect_alerts(events_by_service: Dict[str, List[datetime]],
                  expected_interval_seconds: int = 60,
                  allowed_misses: int = 3) -> List[Dict[str, str]]:
    """Detect when a service misses 3 consecutive expected heartbeats."""
    alerts = []
    interval = timedelta(seconds=expected_interval_seconds)

    for service, timestamps in events_by_service.items():
        if not timestamps:
            continue

        expected = timestamps[0]
        missed_count = 0

        for actual in timestamps[1:]:

            # Count misses until actual heartbeat arrives
            while expected + interval < actual:
                expected = expected + interval
                missed_count += 1

                # If enough misses -> alert
                if missed_count == allowed_misses:
                    alerts.append({
                        "service": service,
                        "alert_at": expected.strftime("%Y-%m-%dT%H:%M:%SZ")
                    })

            # Heartbeat arrives → reset misses
            if actual >= expected:
                expected = actual
                missed_count = 0

    return alerts
