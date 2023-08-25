
from datetime import datetime,timedelta
from django import forms
from .models import *
from userview.models import CustomUser

class DateInput(forms.DateInput):
    input_type = 'date'    



# class CarwashForm(forms.ModelForm):
#     class Meta:
#         model=CarWashPackage
#         fields = ('image', 'name', 'description','vehicle_type','price')
        
class BookingForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%d'),  # Set the minimum date to tomorrow
            'max': (datetime.now().date() + timedelta(days=5)).strftime('%Y-%m-%d'),  # Set the maximum date to five days later
        })
    )
    class Meta :
        model = Booking
        fields = ('make','model','vehicle_no','start_date')
                
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['start_date'].required = False
        

class UserForm(forms.ModelForm):
    
    class Meta : 
        model = CustomUser
        fields = ('first_name','last_name','phone','email')
        
    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs) 
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
class UserProfileForm(forms.ModelForm):
    
    class Meta : 
        model = Userprofile
        fields = ('address_line','city','state','country')
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs) 
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    
