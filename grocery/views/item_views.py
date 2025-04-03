from django.shortcuts import redirect
from django.http import HttpResponse
import datetime
import json
from grocery.utils import load_grocery_list, save_grocery_list, load_order_history, save_order_history
from grocery.models import GroceryItem
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import datetime
from grocery.models import GroceryItem


def add_item(request):
    if request.method == 'POST':
        new_item = request.POST.get('item')
        group = request.POST.get('group')
        try:
            group = int(group)
        except (TypeError, ValueError):
            group = 0
        if new_item:
            items = load_grocery_list()
            items.append({
                'name': new_item,
                'category': group,
                'done': False,
                'order': None,
                'last_done_date': None
            })
            save_grocery_list(items)
        return redirect('index')
    else:
        # For GET requests, simply redirect to the index
        return redirect('index')




def update_status(request):
    if request.method == 'POST':
        item_name = request.POST.get('name')
        # Assumes item names are unique (or you can filter by id)
        item = get_object_or_404(GroceryItem, name__iexact=item_name)
        item.done = True
        item.last_done_date = datetime.date.today()
        # Optionally calculate order (e.g., maximum current order + 1)
        max_order = GroceryItem.objects.filter(last_done_date=datetime.date.today()).aggregate(max_order=models.Max('order'))['max_order'] or 0
        item.order = max_order + 1
        item.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request method"}, status=405)



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
