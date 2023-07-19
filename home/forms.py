
from django import forms
from .models import Vehicle,Order


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'vehicle_type', 'registration_no', 'color']

class OrderForm(forms.ModelForm):
   
    class Meta:
        model = Order
        fields = ['start_date','start_time','order_note']

    

    
