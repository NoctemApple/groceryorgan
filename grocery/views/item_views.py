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
    if request.method == 'POST':
        item_name = request.POST.get('name')
        items = load_grocery_list()
        history = load_order_history()
        current_order = max((data.get('order') or 0 for data in history.values() if data.get('order')), default=0)
        for item in items:
            if item['name'].lower() == item_name.lower():
                item['done'] = True
                item['order'] = current_order + 1
                item['last_done_date'] = datetime.date.today().isoformat()
                history[item['name'].lower()] = {
                    'order': item['order'],
                    'category': item.get('category', 0)
                }
                break
        save_grocery_list(items)
        save_order_history(history)
        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
    return HttpResponse("Invalid request method", status=405)

def undo_status(request):
    if request.method == 'POST':
        item_name = request.POST.get('name')
        items = load_grocery_list()
        history = load_order_history()
        key = item_name.lower()
        for item in items:
            if item['name'].lower() == key:
                item['done'] = False
                item['order'] = history.get(key, {}).get('order')
                item['last_done_date'] = None
                break
        save_grocery_list(items)
        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
    return HttpResponse("Invalid request method", status=405)