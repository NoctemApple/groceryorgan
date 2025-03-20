from .file_utils import load_order_history, save_order_history

def merge_grocery_lists(new_items, old_items):
    """
    Merges new_items with old_items, using persistent history to preserve
    each item's historical order and category.
    """
    history = load_order_history()
    merged = []
    old_lookup = {item['name'].lower(): item for item in old_items}

    for new_item in new_items:
        key = new_item['name'].lower()
        if key in history:
            new_item['order'] = history[key].get('order')
            new_item['category'] = history[key].get('category', new_item.get('category', 0))
        elif key in old_lookup:
            new_item['order'] = old_lookup[key].get('order')
            new_item['category'] = old_lookup[key].get('category', new_item.get('category', 0))
        else:
            new_item['order'] = None
        merged.append(new_item)
    return merged

def update_history_with_insertion(new_items):
    history = load_order_history()
    max_order = max(
        (data.get('order') for data in history.values() if data.get('order') is not None),
        default=0
    )
    for new_item in new_items:
        key = new_item['name'].lower()
        if key in history and history[key].get('order') is not None:
            new_item['order'] = history[key]['order']
        else:
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

    # Merge them back together after sorting individually.
    merged = sorted(items, key=lambda x: x['order'] if x['order'] is not None else float('inf'))

    # Reassign sequential order numbers (1-indexed)
    for index, item in enumerate(merged):
        item['order'] = index + 1

    return merged

def merge_and_preserve_history(new_items):
    """
    For each item in new_items, if it exists in persistent history (i.e. already has an 'order'),
    then keep that order. For new items, assign a new order after the current max.
    """
    history = load_order_history()
    max_order = max(
        (data.get('order') for data in history.values() if data.get('order') is not None),
        default=0
    )
    
    for item in new_items:
        key = item['name'].lower()
        if key in history and history[key].get('order') is not None:
            item['order'] = history[key]['order']
        else:
            max_order += 1
            item['order'] = max_order
            history[key] = {'order': max_order, 'category': item.get('category', 0)}
    
    save_order_history(history)
    new_items.sort(key=lambda x: (x.get('category', 0), x['order']))
    return new_items

def merge_and_resolve_conflicts(items, current_date):
    """
    Separates items into those updated on current_date and those that are not.
    For updated items, assign new order numbers starting after the max order among not-updated.
    Then merge and return the sorted list.
    """
    updated = []
    not_updated = []
    
    for item in items:
        if item.get('last_done_date') == current_date:
            updated.append(item)
        else:
            not_updated.append(item)
    
    max_order = max((item.get('order') or 0 for item in not_updated), default=0)
    updated_sorted = sorted(updated, key=lambda x: x.get('order') if x.get('order') is not None else float('inf'))
    
    for idx, item in enumerate(updated_sorted):
        item['order'] = max_order + idx + 1
    
    merged = not_updated + updated_sorted
    merged.sort(key=lambda x: x.get('order'))
    return merged
