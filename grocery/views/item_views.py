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
        if new_item:
            GroceryItem.objects.create(
                name=new_item,
                category=group,
                done=False,
                order=None,  # New items can have order as None, updated later
                last_done_date=None
            )
        return redirect('index')
    return HttpResponse("Invalid request method", status=405)


def update_status(request):
    if request.method == 'POST':
        item_name = request.POST.get('name')
        items = load_grocery_list()
        history = load_order_history()
        
        # Consider only items that are marked as done in the current session/week
        current_orders = [
            item['order'] for item in items 
            if item.get('order') is not None and item.get('last_done_date') == datetime.date.today().isoformat()
        ]
        current_max_order = max(current_orders, default=0)
        
        for item in items:
            if item['name'].lower() == item_name.lower():
                item['done'] = True
                new_order = current_max_order + 1
                item['order'] = new_order
                history[item_name.lower()] = {
                    'order': new_order,
                    'category': item.get('category', 0)
                }
                item['last_done_date'] = datetime.date.today().isoformat()
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
