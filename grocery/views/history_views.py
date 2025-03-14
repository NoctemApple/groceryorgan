from django.shortcuts import redirect
from django.http import HttpResponse
from grocery.utils import save_grocery_list, save_order_history

def clear_list(request):
    if request.method == 'POST':
        save_grocery_list([])
        return redirect('index')
    return HttpResponse("Invalid request method", status=405)

def clear_history(request):
    if request.method == 'POST':
        save_order_history({})
        return redirect('index')
    return HttpResponse("Invalid request method", status=405)