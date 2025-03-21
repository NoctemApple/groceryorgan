from django.shortcuts import render
from ..models import Group

def add_item_view(request):
    if request.method == 'POST':
        # Handle form submission
        # ...
        pass
    else:
        group_options = Group.objects.all()
        return render(request, 'your_template.html', {'group_options': group_options})
