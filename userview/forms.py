
from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(help_text=None)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password', 'confirm_password']
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].error_messages.clear()
          
          
