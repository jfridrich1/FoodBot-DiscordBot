import json
import os

CONFIG_FILE = "config.json"

# Ak súbor neexistuje, vytvor prázdny
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump({}, f, indent=4)

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)