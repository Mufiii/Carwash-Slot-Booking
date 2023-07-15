import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm, OrderForm
from .models import Order






def place_order(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        order_form = OrderForm(request.POST)

        if customer_form.is_valid() and order_form.is_valid():
            # Save the customer details
            customer = customer_form.save()

            # Create a new order
            order = order_form.save(commit=False)
            order.customer = customer
            order.save()

            return redirect('order_success')  # Redirect to a success page after order placement
    else:
        customer_form = CustomerForm()
        order_form = OrderForm()

    return render(request, 'orders/place_orders.html', {'customer_form': customer_form, 'order_form': order_form})



def myorders(request) :
    return render(request,'orders/order_success.html')


@login_required
def userProfile(request) :
    user = request.user
    context = {
        'user': user
    }
    return render(request,'orders/userprofile.html',context)
