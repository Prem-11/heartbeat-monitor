import json
import argparse
from processor import group_and_sort_events, detect_alerts

def load_events(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    p = argparse.ArgumentParser(description="Heartbeat alert detector")
    p.add_argument("--file", "-f", default="events.json", help="Path to events JSON")
    p.add_argument("--interval", "-i", type=int, default=60, help="expected interval seconds")
    p.add_argument("--misses", "-m", type=int, default=3, help="allowed consecutive misses")
    args = p.parse_args()

    raw = load_events(args.file)
    grouped = group_and_sort_events(raw)
    alerts = detect_alerts(grouped, expected_interval_seconds=args.interval, allowed_misses=args.misses)

    print(json.dumps(alerts, indent=2))

if __name__ == "__main__":
    main()
