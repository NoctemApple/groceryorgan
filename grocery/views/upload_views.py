from django.shortcuts import render, redirect
from grocery.utils import (
    load_grocery_list, parse_grocery_text, merge_grocery_lists,
    save_grocery_list, merge_and_preserve_history, merge_and_resolve_conflicts
)
import datetime

def upload_list(request):
    if request.method == 'POST':
        raw_text = request.POST.get('raw_text')
        if raw_text:
            new_items = parse_grocery_text(raw_text)  # Parse the raw text into list of dicts
            old_items = load_grocery_list()
            merged_items = merge_grocery_lists(new_items, old_items)
            # Reset done status and clear last_done_date if needed
            for item in merged_items:
                item['done'] = False
                item['last_done_date'] = None
            
            # First, preserve historical order for items that already have it
            preserved = merge_and_preserve_history(merged_items)
            
            # Then, resolve conflicts: reassign orders for items updated this week
            current_date = datetime.date.today().isoformat()
            resolved = merge_and_resolve_conflicts(preserved, current_date)
            
            save_grocery_list(resolved)
        return redirect('index')
    return render(request, 'grocery/upload.html')


def merge_grocery_lists(new_items, old_items):
    """
    Merge new_items with old_items, preserving 'order' and other metadata
    for items that existed previously.
    """
    old_lookup = {i['name'].lower(): i for i in old_items}
    merged = []
    for n in new_items:
        key = n['name'].lower()
        if key in old_lookup:
            # preserve old order
            n['order'] = old_lookup[key].get('order')
            n['category'] = old_lookup[key].get('category', n.get('category', 0))
        else:
            # new item, no order
            n['order'] = None
        merged.append(n)

    # Also keep items that are in old_items but not in new_items
    # if you want them to persist (or omit if you want them removed)
    # for o in old_items:
    #     if o['name'].lower() not in [n['name'].lower() for n in new_items]:
    #         merged.append(o)

    return merged
