from django.shortcuts import render, redirect
from django.http import HttpResponse
import json, datetime
from .utils import load_grocery_list, save_grocery_list, parse_grocery_text, merge_grocery_lists


def organize_items(items):
    """
    Organizes items by sorting first on 'category' and then on 'order'.
    Items with no recorded order (order is None) are treated as having an infinite order,
    so they appear after items with an order.
    """
    return sorted(items, key=lambda x: (x.get('category', 0), x['order'] if x['order'] is not None else float('inf')))

def index(request):
    """
    Loads the grocery list from the JSON file, sorts it based on previous order
    (i.e. items with an order appear in ascending order and items with no order at the end),
    and renders the index template.
    """
    items = load_grocery_list()
    sorted_items = sort_by_previous_order(items)
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
                "category": 0,
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
    and recording today's date.
    """
    if request.method == 'POST':
        item_name = request.POST.get('name')
        items = load_grocery_list()
        current_order = max((item.get('order') or 0 for item in items if item.get('order')), default=0)
        for item in items:
            if item['name'].lower() == item_name.lower():
                item['done'] = True
                item['order'] = current_order + 1
                item['last_done_date'] = datetime.date.today().isoformat()
                break
        save_grocery_list(items)
        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
    return HttpResponse("Invalid request method", status=405)

def upload_list(request):
    if request.method == 'POST':
        raw_text = request.POST.get('raw_text')
        if raw_text:
            # Parse the new list from the uploaded text
            new_items = parse_grocery_text(raw_text)
            # Load the existing (old) items
            old_items = load_grocery_list()
            # Merge new items with old items, preserving order metadata
            merged_items = merge_grocery_lists(new_items, old_items)
            # Reset the checklist for the new week:
            for item in merged_items:
                item['done'] = False
                item['last_done_date'] = None
            save_grocery_list(merged_items)
        return redirect('index')
    return render(request, 'grocery/upload.html')



def sort_by_previous_order(items):
    """
    Sort items so that those with a recorded order (not None) appear first 
    in ascending order; items without an order are sorted to the bottom.
    """
    return sorted(items, key=lambda x: x['order'] if x['order'] is not None else float('inf'))

