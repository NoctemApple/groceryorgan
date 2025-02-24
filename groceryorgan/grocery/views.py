from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import load_grocery_list, save_grocery_list, parse_grocery_text
import datetime

def organize_items(items):
    unchecked = [item for item in items if not item.get('done')]
    checked = [item for item in items if item.get('done')]
    checked.sort(key=lambda x: x.get('order', 0))
    return unchecked + checked

def index(request):
    items = load_grocery_list()
    organized = organize_items(items)
    return render(request, 'grocery/index.html', {'grocery_list': organized})

def add_item(request):
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

def upload_list(request):
    if request.method == 'POST':
        raw_text = request.POST.get('raw_text')
        if raw_text:
            items = parse_grocery_text(raw_text)
            save_grocery_list(items)
        return redirect('index')
    return render(request, 'grocery/upload.html')

import json

def update_status(request):
    if request.method == 'POST':
        item_name = request.POST.get('name')
        items = load_grocery_list()
        current_order = max((item.get('order') or 0 for item in items if item.get('order')), default=0)
        for item in items:
            if item['name'] == item_name:
                item['done'] = True
                item['order'] = current_order + 1
                item['last_done_date'] = datetime.date.today().isoformat()
                break
        save_grocery_list(items)
        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
    return HttpResponse("Invalid request method", status=405)
