from django.shortcuts import redirect
from grocery.models import GroceryItem, Group

def add_item(request):
    if request.method == 'POST':
        new_item_name = request.POST.get('item')
        group_id = request.POST.get('group')
        group = Group.objects.filter(id=group_id).first()  # Or choose a default group.
        if new_item_name:
            GroceryItem.objects.create(
                name=new_item_name,
                group=group,
                done=False,
                order=None,
                last_done_date=None
            )
        return redirect('index')
    return redirect('index')
