import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, 'order_history.json')
LIST_FILE = os.path.join(BASE_DIR, 'grocery_list.json')

def load_order_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}  # No history yet

def save_order_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def load_grocery_list():
    if os.path.exists(LIST_FILE):
        with open(LIST_FILE, 'r') as f:
            return json.load(f)
    return []  # No data yet

def save_grocery_list(grocery_list):
    with open(LIST_FILE, 'w') as f:
        json.dump(grocery_list, f, indent=4)

def parse_grocery_text(text):
    """
    Parses the raw text input into a list of items.
    Each non-blank line becomes an item with a 'category' index.
    The category increases by 1 each time a blank line is encountered.
    """
    items = []
    group = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            items.append({
                'name': stripped,
                'category': group,
                'done': False,
                'order': None,
                'last_done_date': None
            })
        else:
            group += 1
    return items

# Merge Function: Merges new items with the old list, preserving metadata (order, category, etc.).
def merge_grocery_lists(new_items, old_items):
    """
    Merges new_items with old_items based on the item name (case-insensitive).
    Uses persistent history (loaded via load_order_history()) to preserve an item's
    historical order and category. If an item exists in history, its order is used;
    if not, and it exists in the old list, that metadata is used. Otherwise, new items
    get order set to None.
    """
    # Load persistent history
    history = load_order_history()
    # Build lookup from old items for fallback
    old_lookup = {item['name'].lower(): item for item in old_items}
    
    merged = []
    for new_item in new_items:
        key = new_item['name'].lower()
        if key in history:
            # Preserve historical order and category
            new_item['order'] = history[key].get('order')
            new_item['category'] = history[key].get('category', new_item.get('category', 0))
        elif key in old_lookup:
            # Fallback: use data from the old list if available
            new_item['order'] = old_lookup[key].get('order')
            new_item['category'] = old_lookup[key].get('category', new_item.get('category', 0))
        else:
            # New item: set order to None
            new_item['order'] = None
        merged.append(new_item)
    return merged
