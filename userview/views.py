from django.shortcuts import redirect, render
from django.urls import path
from django.contrib.auth import authenticate,login
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
                      otp = get_random_string(length=4, allowed_chars='123456789')
                      request.session['otp'] = otp
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
                      
                      
                      user.save()
                            
                      # Redirect to the OTP verification page
                      return redirect('userview/verify_otp', user_id=user.id)
                      
                    else:
                      messages.error(request, "Phone number must be 10 digits")
                  else:
                    messages.error(request, "Password does not match")
               else:
                messages.error(request, "Username must start with an alphabet")
            else:
              messages.error(request, "Username must contain at least 5 characters")
        else:
          # form.errors.clear()
          # form.non_field_errors().clear()
          messages.error(request,"Invalid form data")  
          
    else: 
        form = RegistrationForm()
    return render(request, 'userviews/register.html', {'form': form})
    
  
  
def send_email(subject, message, sender, recipient_list):
    email = EmailMessage(subject, message, sender, recipient_list)
    email.send()


# verify OTP
def verify_otp(request,user_id=0) :
  get_otp = request.session.get('otp')
  print(get_otp)
  user = CustomUser.objects.get(id=user_id)
  
  if request.method == 'POST' :
    otp = request.POST.get('otp')
    if get_otp == otp and  'verify-forgot-otp' not  in request.path :
      del request.session['otp']
      user.is_active = True
      print('thoppi')
      user.save() 
      return redirect('login')
    elif  get_otp == otp and  'verify-forgot-otp' in request.path :
      messages.success(request, 'Enter the Otp that send in the Your Email')
      return redirect('reset',user_id = user.id)
    elif get_otp == otp and 'verify-login-otp' in request.path:
            # Additional logic for 'verify-login-otp' path
            messages.success(request, 'OTP verification successful. Login successful.')
            return redirect('home')
    else:
      messages.error(request, 'Invalid OTP')
      return redirect('verify_otp', user_id=user.id)
  return render(request, 'userviews/verify_otp.html')


def user_login(request) :
  if request.method == 'POST' :
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(email=email,password=password)
    print(user)
    if user is not None :
      login(request,user)
      # send_email(subject, message, sender, recipient_list)
      return redirect('home')
    else:
      messages.error(request ,'Invalid Email or Password')
  
      
  return render(request, 'userviews/login.html' )

#forgot Password
def forgot_password(request) :
  if request.method == 'POST' :
        email = request.POST['email']
        # if CustomUser.objects.filter(email=email).exist() :
        try:
            user = CustomUser.objects.get(email=email)
            print(user)
            otp = get_random_string(length=4, allowed_chars='123456789')
            user.save()
            request.session['otp'] = otp
            subject = 'OTP for Reset Password'
            message = f'Your OTP for password reset is {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_email(subject,message,email_from,recipient_list)
            return redirect('verify_forgot_otp',user_id=user.id)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email does not exist')
            return redirect('forgot')
  return render(request, 'userviews/forgot_password.html')


# reset_password
def reset_password(request,user_id) :
  user = CustomUser.objects.get(id=user_id)
  if request.method == 'POST' :
    password = request.POST['password']
    confirm_password = request.POST['confirm_password'] 
    if password == confirm_password :
      user.set_password(password)
      user.save()
      print(user)
      print(password)
  return render(request,'userviews/reset_password.html', {'user':user})


def home(request) :
  return render(request,'userviews/home.html')


def login_with_otp(request) :
  if request.method == 'POST' :
    email = request.POST['email']
    user = CustomUser.objects.get(email=email)
    if user:
      otp = get_random_string(length=4 , allowed_chars='123456789')
      user.save()
      request.session['otp'] = otp
      subject = 'OTP for Login'
      message = f'This is Your OTP for Login {otp}'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [email,]
      send_email(subject,message,email_from,recipient_list)
      return redirect('userviews/verify_login_otp', user_id = user.id)
      
      
  return render(request,'userviews/loginwithotp.html')



    
    


