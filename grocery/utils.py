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
    history = load_order_history()
    # Get the highest order from history, ignoring items with no order
    max_order = max(
        (data.get('order') for data in history.values() if data.get('order') is not None),
        default=0
    )
    for new_item in new_items:
        key = new_item['name'].lower()
        if key in history and history[key].get('order') is not None:
            # Preserve the historical order if it exists
            new_item['order'] = history[key]['order']
        else:
            # Assign a new order for new items
            max_order += 1
            new_item['order'] = max_order
            history[key] = {'order': max_order, 'category': new_item.get('category', 0)}
    save_order_history(history)
    new_items.sort(key=lambda x: x['order'] if x['order'] is not None else float('inf'))
    return new_items

def merge_and_reassign_orders(items, current_date):
    """
    Recalculates orders by separating items updated on the current_date from those that are not,
    merging them and then reassigning sequential order numbers.
    """
    updated = [item for item in items if item.get('last_done_date') == current_date]
    not_updated = [item for item in items if item.get('last_done_date') != current_date]

    # Sort each list by their current order (with None at the end)
    updated_sorted = sorted(updated, key=lambda x: x['order'] if x['order'] is not None else float('inf'))
    not_updated_sorted = sorted(not_updated, key=lambda x: x['order'] if x['order'] is not None else float('inf'))

    # Merge them back together; adjust this merge logic if you need a specific interleaving
    merged = sorted(items, key=lambda x: x['order'] if x['order'] is not None else float('inf'))

    # Reassign sequential order numbers (1-indexed)
    for index, item in enumerate(merged):
        item['order'] = index + 1

    return merged

def merge_and_preserve_history(new_items):
    """
    For each item in new_items, if it exists in persistent history (i.e. already has an 'order'),
    then keep that order. For new items, assign a new order after the current max.
    Finally, sort items by category and order.
    """
    history = load_order_history()
    # Determine the current max order among items with an order
    max_order = max(
        (data.get('order') for data in history.values() if data.get('order') is not None),
        default=0
    )
    
    for item in new_items:
        key = item['name'].lower()
        if key in history and history[key].get('order') is not None:
            # Preserve the existing order
            item['order'] = history[key]['order']
        else:
            # New item: assign a new order
            max_order += 1
            item['order'] = max_order
            history[key] = {'order': max_order, 'category': item.get('category', 0)}
    
    # Save updated history
    save_order_history(history)
    
    # Sort items by category first, then by order (lower order numbers come first)
    new_items.sort(key=lambda x: (x.get('category', 0), x['order']))
    return new_items
