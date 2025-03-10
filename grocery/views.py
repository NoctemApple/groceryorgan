from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import json
from .utils import (
    load_grocery_list,
    save_grocery_list,
    parse_grocery_text,
    merge_grocery_lists,
    load_order_history,
    save_order_history,
)

def organize_items(items):
    return sorted(items, key=lambda x: (x.get('category', 0), x['order'] if x['order'] is not None else float('inf')))

def index(request):
    """
    Loads the grocery list, sorts it based on group (category) and then historical order,
    and renders the index template.
    """
    items = load_grocery_list()
    sorted_items = organize_items(items)
    return render(request, 'grocery/index.html', {'grocery_list': sorted_items})

def add_item(request):
    """
    Handles adding a single item to the grocery list.
    """
    if request.method == 'POST':
        new_item = request.POST.get('item')
        items = load_grocery_list()
        if new_item:
            items.append({
                "name": new_item,
                "category": 0,  # Default to group 0 for single items
                "done": False,
                "order": None,
                "last_done_date": None
            })
            save_grocery_list(items)
        return redirect('index')
    return HttpResponse("Invalid request method", status=405)

def update_status(request):
    """
    Marks an item as done by updating its 'done' flag, assigning an order,
    and recording today's date. Also updates the historical order mapping.
    """
    if request.method == 'POST':
        item_name = request.POST.get('name')
        items = load_grocery_list()
        history = load_order_history()
        # Determine the current highest order from history
        current_order = max((data.get('order') or 0 for data in history.values() if data.get('order')), default=0)
        for item in items:
            if item['name'].lower() == item_name.lower():
                item['done'] = True
                item['order'] = current_order + 1
                item['last_done_date'] = datetime.date.today().isoformat()
                # Update the history so that this order persists
                history[item['name'].lower()] = {
                    'order': item['order'],
                    'category': item.get('category', 0)
                }
                break
        save_grocery_list(items)
        save_order_history(history)
        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
    return HttpResponse("Invalid request method", status=405)

def upload_list(request):
    """
    Processes an uploaded full list:
      - Parses the raw text into items with group numbers.
      - Merges them with the existing list (preserving historical order and category when available).
      - Resets the 'done' status and 'last_done_date' for the new week.
    """
    if request.method == 'POST':
        raw_text = request.POST.get('raw_text')
        if raw_text:
            new_items = parse_grocery_text(raw_text)
            old_items = load_grocery_list()
            merged_items = merge_grocery_lists(new_items, old_items)
            # Reset the done status for the new week without losing historical order.
            for item in merged_items:
                item['done'] = False
                item['last_done_date'] = None
            save_grocery_list(merged_items)
        return redirect('index')
    return render(request, 'grocery/upload.html')

def undo_status(request):
    """
    Reverts an item's 'done' status by resetting its order and last_done_date.
    Also updates persistent history accordingly.
    """
    if request.method == 'POST':
        item_name = request.POST.get('name')
        items = load_grocery_list()
        history = load_order_history()
        key = item_name.lower()
        # Look for the item in the current list.
        for item in items:
            if item['name'].lower() == key:
                item['done'] = False
                # Optionally, you might decide not to reset the order in history,
                # so that if the user marks it done again later, it reuses the old order.
                # Here we choose to leave history intact so that undo doesn't remove history.
                item['order'] = history.get(key, {}).get('order')
                item['last_done_date'] = None
                break
        save_grocery_list(items)
        # Do not clear history here because we want to preserve past order.
        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
    return HttpResponse("Invalid request method", status=405)

def clear_list(request):
    """
    Clears the current grocery list and (optionally) the order history.
    Use with caution!
    """
    if request.method == 'POST':
        # Clear the grocery list.
        save_grocery_list([])
        # Optionally, clear the persistent history as well.
        # Uncomment the next line if you want to clear history too.
        # save_order_history({})
        return redirect('index')
    return HttpResponse("Invalid request method", status=405)

def clear_history(request):
    """
    Clears the persistent order history.
    """
    if request.method == 'POST':
        # Clear the order history by saving an empty dictionary.
        save_order_history({})
        return redirect('index')
    return HttpResponse("Invalid request method", status=405)

def add_item(request):
    """
    Handles adding a single item to the grocery list with a specified group.
    """
    if request.method == 'POST':
        new_item = request.POST.get('item')
        group = request.POST.get('group')
        try:
            group = int(group)
        except (TypeError, ValueError):
            group = 0
        items = load_grocery_list()
        if new_item:
            items.append({
                "name": new_item,
                "category": group,  # use 'group' as the category
                "done": False,
                "order": None,
                "last_done_date": None
            })
            save_grocery_list(items)
        return redirect('index')
    return HttpResponse("Invalid request method", status=405)

def get_group_options(items):
    """
    Returns a sorted list of unique group numbers from the given items.
    If no items exist, returns [0] as the default group.
    """
    if not items:
        return [0]
    groups = set(item.get('category', 0) for item in items)
    return sorted(list(groups))

def index(request):
    """
    Loads the grocery list, sorts it, and passes the list along with available group options.
    """
    items = load_grocery_list()
    sorted_items = organize_items(items)
    group_options = get_group_options(items)
    return render(request, 'grocery/index.html', {
        'grocery_list': sorted_items,
        'group_options': group_options
    })

def add_item(request):
    if request.method == 'POST':
        new_item = request.POST.get('item')
        group = request.POST.get('group')
        try:
            group = int(group)
        except (TypeError, ValueError):
            group = 0
        items = load_grocery_list()
        if new_item:
            items.append({
                "name": new_item,
                "category": group,
                "done": False,
                "order": None,
                "last_done_date": None
            })
            save_grocery_list(items)
        return redirect('index')
    return HttpResponse("Invalid request method", status=405)
