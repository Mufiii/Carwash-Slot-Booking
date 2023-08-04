import datetime
from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import razorpay
from home.models import *
from .models import *
from .forms import *
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.


def place_order(request,id,pack_id):
  order = Booking.objects.get(id = id)
  
  packages = CarWashPackage.objects.get(pk=pack_id)
  print("first----->",order)
  print("second",packages)

  if request.method == 'POST':
      print(request.POST)
      form = OrderForm(request.POST)
      if form.is_valid():
          data = form.save(commit=False)
           # Generate Order Number 
          yr = int(datetime.date.today().strftime('%Y'))
          dt = int(datetime.date.today().strftime('%d'))
          mt = int(datetime.date.today().strftime('%m'))
          d = datetime.date(yr,mt,dt)
          current_date = d.strftime("%Y%m%d")
          order_number = current_date + str(data.id)
          data.order_number = order_number
        
          data.save()
          return redirect('checkout',  order_id=data.id, booking_id=id)
        
      else :
        print(form.errors)
  else :
     form = OrderForm()
  
  context = {
        'form': form,
        'order': order,
        'packages':packages
    }     
  return render(request, 'order/place_order.html',context)


def checkout(request,order_id,booking_id):
    user = request.user
    data = get_object_or_404(OrderDetails, id=order_id)
    booking = get_object_or_404(Booking,id=booking_id)
    # print(booking_id)
    # print(order_id)

    grant_totel = 0
    total = booking.package.price 

    tax = (2 * total)/100
    grant_totel = total + tax

    # print(grant_totel)

    client = razorpay.Client(auth =(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
    payment = client.order.create({'amount':int(grant_totel)*100,'currency':'INR' , 'payment_capture':1})
    key_id = settings.RAZOR_PAY_KEY_ID
    


    context = {
    'user':user,
    'data': data,
    'booking': booking,
    'payment': payment,
    'booking_id': booking_id,
    'order_id': order_id,
    'grand_total': grant_totel, 
    'tax': tax, 
    }
    return render(request, 'order/checkout.html',context)

    
  
  
def success(request):
  
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    booking_id = request.GET.get('booking_id')
    order_id = request.GET.get('order_id')
    try:
        # Use the correct field for filtering the Booking model
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Rest of your code...
    except Booking.DoesNotExist:
        pass
      
    print("razorpay_order_id:", razorpay_order_id)
    print("booking_id:", booking_id)
    
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    
    try :
      payment = client.payment.fetch(razorpay_payment_id)
      
      amount_paid = payment['amount'] /100 # Amount is in paise, so convert to rupees
      razorpay_status = payment['status']
      print(razorpay_status,amount_paid,payment,'blaaaaaah')
      
      PaymentDetail.objects.create(
        razorpay_payment_id=razorpay_payment_id,
        user=request.user,  # Assuming Booking has a user field
        package=booking.package,
        booking=booking,
        amount_paid=amount_paid,
        razor_pay_status=razorpay_status
      )
      
      booking.is_paid = True
      booking.save()
      
      mail_subject = "Your booking receipt"
      context = {
        'user': booking.user,
        'booking': booking,
        'amount_paid': amount_paid,
      }    
      message = render_to_string('order/receipt_email.html', context)
      from_email = settings.EMAIL_HOST_USER
      to_email = [booking.user.email]

      email = EmailMessage(mail_subject, message, from_email, to_email)
      email.send()

      
    except razorpay.errors.BadRequestError as e:
        return HttpResponse(f'Error: {str(e)}')
    
    context = {
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_order_id': razorpay_order_id,
    }
    return render(request, 'order/success.html', context)
  

    
  