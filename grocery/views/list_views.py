from django.shortcuts import render
from grocery.utils import load_grocery_list

def organize_items(items):
    return sorted(items, key=lambda x: (
        x.get('category', 0),
        x['order'] if x['order'] is not None else float('inf')
    ))


def get_group_options(items):
    if not items:
        return [0]
    groups = set(item.get('category', 0) for item in items)
    return sorted(list(groups))

def index(request):
    items = load_grocery_list()
    sorted_items = organize_items(items)
    return render(request, 'grocery/index.html', {'grocery_list': sorted_items})
