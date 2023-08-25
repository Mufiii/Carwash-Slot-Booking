from django.core.cache import cache
import time
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path
from django.contrib.auth import authenticate,login
from CarWash import settings 
from .models import CustomUser
from home.models import Booking
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
import re
import pyotp
from django.core.mail import EmailMessage
from BruteBuster.models import FailedAttempt



@never_cache
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
            if len(username) >= 5 and re.match(r'^[A-Za-z]', username):
              if len(password) >= 8 and re.search(r'[A-Z].*[a-z].*\d', password):
                  if password == confirm_password :
                    if re.match(r'^\d{10}$', phone) and not re.search(r'\D', phone):
                        
                        totp = pyotp.TOTP(pyotp.random_base32())
                        # otp_secret_key = totp.secret
                        # print('otp_secret_key',otp_secret_key)
                        otp = totp.now()
                        print('otp',otp)
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
                        message = f'Your OTP for Account Verification {otp}'  # Make sure 'otp' is the correct variable
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [email]
                        send_email(subject, message, email_from, recipient_list)
                      
                      
                        user.save()
                            
                      # Redirect to the OTP verification page
                        return redirect('verify_otp', user_id=user.id ,verification='register')
                      
                    else:
                      messages.error(request, "Phone number must be 10 digits")
                  else:
                    messages.error(request, "Password does not match")
              else:
                  messages.error(request,"Password should contain at least one uppercase letter, one lowercase letter, and one digit")
            else:            
              messages.error(request, "Username must contain at least 5 characters")
        # else:
        #   messages.error(request,"Invalid Data")  
          
    else: 
        form = RegistrationForm()
    return render(request, 'userviews/register.html', {'form': form})
    
  
  
  
def send_email(subject, message, sender, recipient_list):
    email = EmailMessage(subject, message, sender, recipient_list)
    email.send()




def verify_otp(request,user_id,verification=None) :
  user = get_object_or_404(CustomUser, id=user_id)
  secret_key = request.session.get('otp')
  
  
  if request.method == 'POST' :
      otp = request.POST.get('otp')
      totp = pyotp.TOTP(secret_key)
      
      print("Entered OTP:", otp)
      print("Generated OTP:", totp)
      print("Secret Key:", secret_key)
      if otp==secret_key:
          if verification == 'register':
              user.is_active = True
              user.save()
              return redirect ('login')
          elif verification == 'forgot':
              return redirect('reset',user_id=user.id)
          elif verification == 'login':
                login(request, user)
                # messages.success(request, 'OTP verification successfull. Login successful.')
                return redirect('home')
      else:
        messages.error(request, 'Invalid OTP, Please try again.')
        return redirect('verify_otp', user_id=user.id,verification=verification)
  return render(request,'userviews/verify_otp.html',{'user': user, 'verification': verification})



# def resend_otp(request, user_id):
#     user = CustomUser.objects.get(id=user_id)
#     secret_key = pyotp.random_base32()
            
#     totp = pyotp.TOTP(secret_key, interval=60)
#     otp = totp.now()
#     request.session['otp_secret_key'] = secret_key
#     request.session['otp'] = otp
#     subject = 'OTP for Login'
#     message = f'This is Your OTP for Login {otp}'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_email(subject, message, email_from, recipient_list)
    
#     return render(request, 'verify.html')

    


def user_login(request) :
    if request.user.is_authenticated:
          return redirect('home')
    if request.method == 'POST' :
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email,password=password)
        print(user)
        if user is not None : 
            login(request,user)
            # messages.success(request,'You are Loggined successfully')
            return redirect('home')
        else:
            fails = FailedAttempt.objects.filter(username=email).values()
            f = fails[0]['failures']
            if fails and f <3 :
                messages.error(request,f'failedattempt {f}')
            elif f>=3 :
                messages.error(request,'Your Account is blocked')
            else:
                messages.error(request ,'Invalid Email or Password')
        
    return render(request, 'userviews/login.html' )


#forgot Password
def forgot_password(request) :
  if request.method == 'POST' :
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
            secret_key = pyotp.random_base32()
            
            totp = pyotp.TOTP(secret_key, interval=60)
            otp = totp.now()
            request.session['otp_secret_key'] = secret_key
            request.session['otp'] = otp
            subject = 'OTP for Reset Password'
            message = f'Your OTP for password reset is {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_email(subject,message,email_from,recipient_list)
            return redirect('verify_forgot_otp',user_id=user.id, verification='forgot')
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
    
    if password != confirm_password :
        messages.error(request,'Password does not match')
    elif user.check_password(password) :
        messages.error(request, "New password must be different from the current password.")
    else :
      user.set_password(password)
      user.save()
      messages.success(request, 'Password successfully reset. You can now log in.')
      return redirect('login')

  return render(request,'userviews/reset_password.html', {'user':user})



def delete_booking(request):
    booking = Booking.objects.filter(is_paid=False) 
    booking.delete()
    return 



@login_required(login_url='login')
@never_cache
def home(request) :
    delete_booking(request)
    # banners = Banner.objects.all()
    # context = {
    #     'banners':banners
    # }
    return render(request,'userviews/home.html')


def login_with_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
            secret_key = pyotp.random_base32()

            totp = pyotp.TOTP(secret_key, interval=60)
            otp = totp.now()

            request.session['otp_secret_key'] = secret_key
            request.session['otp'] = otp
            
            subject = 'OTP for Login'
            message = f'This is Your OTP for Login {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_email(subject, message, email_from, recipient_list)

            return redirect('verify_otp', user_id=user.id, verification='login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login_with_otp')
    return render(request, 'userviews/loginwithotp.html')



def logout_view(request):
    logout(request)
    return redirect('home')
  

  



    
    


