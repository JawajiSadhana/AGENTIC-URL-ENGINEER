import json
MEMORY_FILE = "agent_memory.json"

def save_state(key, value):
    try:
        with open(MEMORY_FILE, "r") as f: data = json.load(f)
    except: data = {}
    data[key] = value
    with open(MEMORY_FILE, "w") as f: json.dump(data, f)

def load_state(key):
    try:
        with open(MEMORY_FILE, "r") as f: data = json.load(f)
        return data.get(key)
    except: return None