import json
from datetime import datetime
import os
LOG_FILE = "logs/traces.jsonl"
os.makedirs("logs", exist_ok=True)

def log(step: str, task: str, status: str):
    entry = {"timestamp": datetime.now().isoformat(), "step": step, "task": task, "status": status}
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")