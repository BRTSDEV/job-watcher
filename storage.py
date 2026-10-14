# db // remember the jobs
import json
from pathlib import Path

SEEN_FILE = Path("seen_jobs.json")

def load_seen():
    if not SEEN_FILE.exists():
        return set()
    try:
        with open(SEEN_FILE, encoding="utf-8") as f:
            return set(json.load(f))
    except json.JSONDecodeError:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, indent=2)