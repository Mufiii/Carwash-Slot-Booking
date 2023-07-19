import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Order



def place_order (request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST) 
        vehicle_form = VehicleForm(request.POST) 
        if vehicle_form.is_valid() and order_form.is_valid():
            vehicle = vehicle_form.save(commit=False)
            vehicle.customer = request.user
            vehicle.save()
            
            order = order_form.save(commit=False)
            order.user = request.user
            order.vehicle = vehicle
            order.save()
            return redirect('myorders')
        else:
            print(vehicle_form.errors)
    else:
        order_form = OrderForm()
        vehicle_form = VehicleForm()

    context = {
        'vehicle_form': vehicle_form,
        'order_form': order_form,
    }        
    return render(request,'orders/place_orders.html',context)



def myorders(request) :
    return render(request,'orders/order_success.html')


@login_required
def userProfile(request) :
    user = request.user
    context = {
        'user': user
    }
    return render(request,'orders/userprofile.html',context)
