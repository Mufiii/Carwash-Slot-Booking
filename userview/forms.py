
import re
from django import forms
from django.forms import ModelForm
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class' : 'form-control', #form will give a css of that particular class
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class' : 'form-control'
    }))
    
    username = forms.CharField(help_text=None)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password', 'confirm_password']
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['placeholder'] = "First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'username@example.com'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].error_messages.clear()
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        
        
          
          
