from django.shortcuts import render, redirect
from grocery.utils import load_grocery_list, parse_grocery_text, merge_grocery_lists, save_grocery_list

def upload_list(request):
    if request.method == 'POST':
        raw_text = request.POST.get('raw_text')
        if raw_text:
            new_items = parse_grocery_text(raw_text)
            old_items = load_grocery_list()
            merged_items = merge_grocery_lists(new_items, old_items)
            for item in merged_items:
                item['done'] = False
                item['last_done_date'] = None
            save_grocery_list(merged_items)
        return redirect('index')
    return render(request, 'grocery/upload.html')