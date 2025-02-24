import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), 'grocery_list.json')

def load_grocery_list():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []  # No data yet

def save_grocery_list(grocery_list):
    with open(DATA_FILE, 'w') as f:
        json.dump(grocery_list, f, indent=4)

def parse_grocery_text(text):
    groups = []
    current_group = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            # Each item becomes a dict with initial values
            current_group.append({
                "name": line,
                "category": len(groups),  # Use group index as category
                "done": False,
                "order": None,
                "last_done_date": None
            })
        else:
            if current_group:
                groups.extend(current_group)
                current_group = []
    if current_group:
        groups.extend(current_group)
    return groups

