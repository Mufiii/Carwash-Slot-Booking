import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Order
from orders.forms import Orderform

# Create your views here.

def place_order(request) :
    current_user = request.user
    form = Orderform(request.POST)
    
    if request.method == 'POST' :
        if form.is_valid():
            data = form.save(commit=False)
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.category = form.cleaned_data['category']
            data.make = form.cleaned_data['make']
            data.model = form.cleaned_data['model']
            data.registration_no = form.cleaned_data['registration_no']
            data.color = form.cleaned_data['color']
            data.start_time = form.cleaned_data['start_time']
            data.last_time = form.cleaned_data['last_time']
            data.save()
            print(data)
            # Generate Order Number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,dt,mt)
            current_date = d.strftime('%y%m%d') 
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('myorders')
        else :
            form = Orderform() 
    return render(request,'orders/orders.html' , {'form':form})


def myorders(request) :
    return render(request,'orders/myorders.html')


def userProfile(request) :
    return render(request,'orders/userprofile.html')
