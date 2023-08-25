from django import forms
from .models import *

class OrderForm(forms.ModelForm):
  order_note = forms.CharField(
    widget=forms.Textarea(attrs={'required':False})
  )
  
  class Meta:
    model = OrderDetails
    fields = ('first_name','last_name','phone','email','address','street','building','zip','city','state','country','order_note')
    
  def __init__(self,*args,**kwargs) :
        super(OrderForm,self).__init__(*args,**kwargs)
        for field in self.fields:
          self.fields[field].widget.attrs['class'] = 'form-control'
          self.fields[field].required = True
          
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['address'].widget.attrs['placeholder'] = 'Address'
        self.fields['street'].widget.attrs['placeholder'] = 'Street'
        self.fields['building'].widget.attrs['placeholder'] = 'Building'
        self.fields['zip'].widget.attrs['placeholder'] = 'ZIP code'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['country'].widget.attrs['placeholder'] = 'Country'
        self.fields['order_note'].widget.attrs['placeholder'] = 'Add any notes for your order'        