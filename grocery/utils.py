import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, 'order_history.json')
LIST_FILE = os.path.join(BASE_DIR, 'grocery_list.json')

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

def parse_grocery_text(text):
    """
    Parses the raw text input into a list of items.
    Each non-blank line becomes an item with a 'category' index.
    The category increments each time a blank line is encountered.
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

def merge_grocery_lists(new_items, old_items):
    """
    Merges new_items with old_items, using persistent history to preserve
    each item's historical order and category. If an item exists in history,
    its order and category are applied. Otherwise, 'order' remains None.
    """
    history = load_order_history()
    merged = []
    old_lookup = {item['name'].lower(): item for item in old_items}

    for new_item in new_items:
        key = new_item['name'].lower()
        if key in history:
            # Use historical order and category if they exist
            new_item['order'] = history[key].get('order')
            new_item['category'] = history[key].get('category', new_item.get('category', 0))
        elif key in old_lookup:
            # If it's in old_items but not in history, preserve the old list's metadata
            new_item['order'] = old_lookup[key].get('order')
            new_item['category'] = old_lookup[key].get('category', new_item.get('category', 0))
        else:
            # New item; no historical order yet
            new_item['order'] = None
        merged.append(new_item)

    # Optionally, keep items from old_items that are missing in new_items (comment out if undesired)
    # for old_item in old_items:
    #     old_key = old_item['name'].lower()
    #     if old_key not in [ni['name'].lower() for ni in new_items]:
    #         merged.append(old_item)

    return merged

def update_history_with_insertion(new_items):
    """
    Overwrites the historical order with the new list's positions.
    For each item in new_items:
      - The 'order' is set to index+1 (the position in the new list).
      - The 'category' is preserved from history if it exists.
      - The updated values are saved to history.
    Finally, new_items is sorted by 'order' and returned.
    """
    history = load_order_history()

    # Keep track of old categories to preserve them if item already existed
    old_categories = {k: v.get('category', 0) for k, v in history.items()}

    for index, new_item in enumerate(new_items):
        key = new_item['name'].lower()
        # Overwrite order with new position
        new_item['order'] = index + 1
        # Preserve old category if it existed
        old_cat = old_categories.get(key, new_item.get('category', 0))
        new_item['category'] = old_cat

        # Update or create history entry
        history[key] = {
            'order': new_item['order'],
            'category': new_item['category']
        }

    # Save the updated history
    save_order_history(history)

    # Return new_items sorted by order
    new_items.sort(key=lambda x: x['order'] if x['order'] is not None else float('inf'))
    return new_items
