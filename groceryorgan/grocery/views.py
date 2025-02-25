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
