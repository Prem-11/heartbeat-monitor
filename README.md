# heartbeat-monitor
A lightweight Python-based heartbeat monitoring tool that detects missing service heartbeats. Each service is expected to send a heartbeat at fixed intervals. If three consecutive heartbeats are missed, the system automatically triggers an alert with the exact timestamp of failure.
