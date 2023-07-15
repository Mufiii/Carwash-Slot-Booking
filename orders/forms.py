
from django import forms
from .models import *
    
from django import forms
from .models import Order, Customer

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'vehicle', 'order_number', 'order_note', 'start_time', 'end_time', 'category']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'city', 'state', 'country']
        
    
