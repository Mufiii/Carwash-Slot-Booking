
import re
from django import forms
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
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email Address'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Your Phone'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Your Username'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5 or not re.match(r'^[A-Za-z]', username):
            raise forms.ValidationError("Username must contain at least 5 characters and start with a letter.")
        return username 
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or not re.search(r'[A-Z].*[a-z].*\d', password):
            raise forms.ValidationError("Password should contain at least one uppercase letter, one lowercase letter, and one digit.")
        return password
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d{10}$', phone) or re.search(r'\D', phone):
            raise forms.ValidationError("Phone number must be 10 digits and contain only digits.")
        return phone
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "password do not match"
            )
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].error_messages.clear()
          
          
