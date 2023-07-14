
from django import forms
from .models import *
    
class Orderform(forms.ModelForm) :
  class Meta :
    model = Order
    fields = '__all__'
    
