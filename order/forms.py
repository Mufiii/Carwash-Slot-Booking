from django import forms
from .models import *

class OrderForm(forms.ModelForm):
  
  class Meta:
    model = OrderDetails
    fields = ('first_name','last_name','phone','email','address','city','state','country','order_note')