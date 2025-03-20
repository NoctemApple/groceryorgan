import json
import os
from .constants import HISTORY_FILE, LIST_FILE

def load_order_history():
    """Load the persistent order history (order_history.json)."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}  # No history yet

def save_order_history(history):
    """Save the persistent order history to order_history.json."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def load_grocery_list():
    """Load the current grocery list from grocery_list.json."""
    if os.path.exists(LIST_FILE):
        with open(LIST_FILE, 'r') as f:
            return json.load(f)
    return []  # No data yet

def save_grocery_list(grocery_list):
    """Save the current grocery list to grocery_list.json."""
    with open(LIST_FILE, 'w') as f:
        json.dump(grocery_list, f, indent=4)
