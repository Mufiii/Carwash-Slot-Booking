from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from CarWash import settings
from .models import CustomUser
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
import re
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            
            # Access other form fields
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if len(username) >= 5:
               if re.match(r'^[A-Za-z]', username):
                  if password == confirm_password :
                    if re.match(r'^\d{10}$', phone):
                      # Generate OTP
                      otp = get_random_string(length=4, allowed_chars='1234567890')
                      user = CustomUser.objects.create_user(
                          first_name=first_name,
                          last_name=last_name,
                          email=email,
                          phone=phone,
                          username=username,
                          password=password
                      )
                      subject = 'OTP for Account verification'
                      message = f'Your OTP for Account Verification {otp}'
                      email_from = settings.EMAIL_HOST_USER
                      recipient_list = [email,]
                      send_email(subject,message,email_from,recipient_list)
                      
                      print(otp)
                      # Store the OTP in the user object
                      user.otp = otp
                      user.save()
                            
                            # Redirect to the OTP verification page
                      return redirect('verify_otp', user_id=user.id)
                      
                    else:
                      messages.error(request, "Phone number must be 10 digits")
                  else:
                    messages.error(request, "Password does not match")
               else:
                messages.error(request, "Username must start with an alphabet")
            else:
              messages.error(request, "Username must contain at least 5 characters")
        else:
          messages.error(request,"Invalid form data")  
          
    else: 
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})
  
  
def send_email(subject, message, sender, recipient_list):
    email = EmailMessage(subject, message, sender, recipient_list)
    email.send()


def verify_otp(request,user_id) :
  
  user = CustomUser.objects.get(id=user_id)
  
  if request.method == 'POST' :
    otp = request.POST.get('otp')
    if user.otp == otp :
      user.is_verified = True
      user.otp = ''
      user.save() 
      messages.success(request, 'Account has been verified')
      return redirect('login')
    else :
      messages.error(request, 'invalid OTP')
      return redirect('verify_otp', user_id=user.id)
  return render(request, 'verify_otp.html', {'user': user})

def login(request) :
  form = RegistrationForm()
  if request.method == 'POST' :
    form = RegistrationForm(request.POST)
    if form.is_valid() :
      email = request.method.get['email']
      password = request.method.get['password']
      
      user = authenticate(request,email=email,password=password)
      
      if user is not None :
        login(request,user)
        return redirect('home')
      else :
        messages.error(request , 'Invalid Email or Password')
  
  else :
    form = RegistrationForm()
    
    
  return render(request, 'login.html' ,{'form':form})



# Email Activation

# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = CustomUser.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None
    
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, "Congratulations! Your account has been activated.")
#         return redirect('login')
#     else:
#         messages.error(request, "Invalid activation link.")
#         return redirect('register')

    
    


