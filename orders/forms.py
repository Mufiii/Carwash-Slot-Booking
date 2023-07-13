
from django import forms
from .models import *

class CategoryForm(forms.ModelForm) :
  
  class Meta :
    model = Category
    fields = ('name',)
    
#VehicleForm
class VehicleForm(forms.Modelform):
  
  class Meta :
    model = Vehicle
    fields = ('make','model','registration_no','color')
    
class Orderform(forms.ModelForm) :
  
    
