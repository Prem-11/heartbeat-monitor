# Heartbeat Monitor

A lightweight Python-based heartbeat monitoring tool that detects missing service heartbeats.  
Each service is expected to send a heartbeat at fixed intervals.  
If three consecutive heartbeats are missed, the system triggers an alert with the exact timestamp.

# Setup Instructions

Follow the steps below to set up and run this project locally.

---

## 1. Open Command Prompt / Terminal

Navigate to the project directory:

cd your-project-folder

## 2. Create a Virtual Environment (Python)

### Windows
python -m venv venv

## 3. Activate the Virtual Environment

### Windows
venv\Scripts\activate

### macOS / Linux
source venv/bin/activate

## 4. Install Dependencies
Make sure requirements.txt is present in the root folder.

### Windows
pip install -r requirements.txt

## 5. Run the Main Program
To run the main solution:
python main.py --file events.json --interval 60 --misses 3

If your system uses python3:
python3 main.py --file events.json --interval 60 --misses 3

## 6. Run Test Cases
Run a specific test file:
python -m unittest tests/test_alerts.py

## 7. Deactivate Virtual Environment (Optional)
deactivate


