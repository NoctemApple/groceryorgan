from django.shortcuts import redirect
from django.http import HttpResponse
import datetime
import json
from grocery.utils import load_grocery_list, save_grocery_list, load_order_history, save_order_history

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

def update_status(request):
    """
    Marks an item as done, assigns a new order if not already set, and updates persistent history.
    """
    if request.method == 'POST':
        item_name = request.POST.get('name')
        items = load_grocery_list()
        history = load_order_history()
        key = item_name.lower()
        
        # If the item already has a historical order, we don't change it.
        if key in history and history[key].get('order') is not None:
            new_order = history[key]['order']
        else:
            # Calculate a new order: find the current maximum order in history and add 1.
            current_order = max(
                [data.get('order', 0) for data in history.values() if data.get('order') is not None] or [0]
            )
            new_order = current_order + 1
        
        for item in items:
            if item['name'].lower() == key:
                item['done'] = True
                item['order'] = new_order
                item['last_done_date'] = datetime.date.today().isoformat()
                # Update history with the new order and preserve category.
                history[key] = {'order': new_order, 'category': item.get('category', 0)}
                break
        save_grocery_list(items)
        save_order_history(history)
        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
    return HttpResponse("Invalid request method", status=405)


def undo_status(request):
    """
    Reverts an item's 'done' status. The historical order remains unchanged.
    """
    if request.method == 'POST':
        item_name = request.POST.get('name')
        items = load_grocery_list()
        history = load_order_history()
        key = item_name.lower()
        for item in items:
            if item['name'].lower() == key:
                item['done'] = False
                # Optionally, you may choose not to clear the order so that it remains for future reference.
                # Here we leave history intact.
                item['last_done_date'] = None
                break
        save_grocery_list(items)
        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
    return HttpResponse("Invalid request method", status=405)
