from django.shortcuts import render
from grocery.utils import load_grocery_list

def get_group_options(items):
    """
    Extract a sorted list of unique group numbers from the items.
    If there are no items, returns [0] as the default group.
    """
    if not items:
        return [0]
    groups = set(item.get('category', 0) for item in items)
    return sorted(list(groups))

def organize_items(items):
    """
    Sort items first by their category (group) and then by their order.
    Items with no order (None) are placed at the end.
    """
    return sorted(items, key=lambda x: (
        x.get('category', 0),
        x['order'] if x['order'] is not None else float('inf')
    ))

def index(request):
    grocery_list = load_grocery_list()

    # Compute existing groups from the grocery list.
    if grocery_list:
        existing_groups = {item.get('category', 0) for item in grocery_list}
        max_group = max(existing_groups)
    else:
        max_group = 0

    # Create group options as a list from 0 to max_group + 1.
    # For example, if max_group is 1, this list becomes [0, 1, 2].
    group_options = list(range(0, max_group + 2))

    sorted_items = organize_items(grocery_list)
    context = {
        'grocery_list': sorted_items,
        'group_options': group_options,
    }
    return render(request, 'grocery/index.html', context)

