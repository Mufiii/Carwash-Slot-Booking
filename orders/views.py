from django.http import HttpResponse
from django.shortcuts import render
from .models import Order
from orders.forms import Orderform

# Create your views here.

def place_order(request) :
    current_user = request.user
    
    if request.method == 'POST' :
        form = Orderform(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data('first_name')
            last_name = form.cleaned_data('last_name')
            phone = form.cleaned_data('phone')
            email = form.cleaned_data('email')
            address = form.cleaned_data('address')
            city = form.cleaned_data('city')
            state = form.cleaned_data('state')
            country = form.cleaned_data('country')
            make = form.cleaned_data('make')
            model = form.cleaned_data('model')
            registration_no = form.cleaned_data('registration_no')
            color = form.cleaned_data('color')
            
    return render(request,'orders/orders.html')

  