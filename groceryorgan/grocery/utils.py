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

 

# This is the test branch right?

def merge_grocery_lists(new_items, old_items):
    """
    Merges new_items with old_items based on the item name (case-insensitive).
    If an item exists in the old list, preserve its 'order' and 'category'.
    Items that are not present in the new upload are dropped.
    """
    old_lookup = {item['name'].lower(): item for item in old_items}
    merged = []
    for new_item in new_items:
        key = new_item['name'].lower()
        if key in old_lookup:
            # Preserve the old category and order
            new_item['category'] = old_lookup[key].get('category', new_item.get('category', 0))
            new_item['order'] = old_lookup[key].get('order')
            new_item['done'] = old_lookup[key].get('done', False)
            new_item['last_done_date'] = old_lookup[key].get('last_done_date')
        merged.append(new_item)
    return merged


