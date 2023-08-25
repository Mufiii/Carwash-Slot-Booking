import datetime
from django.contrib import messages
from smtplib import SMTPResponseException
from django.core.mail import EmailMessage
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import razorpay
from home.models import *
from userview.views import send_email
from .models import *
from .forms import *
from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa
# Create your views here.


def place_order(request):

  if request.method == 'POST':
      print(request.POST)
      print("erdfxxxxxxxfgtcvghbygyughyguj")
      form = OrderForm(request.POST)
      if form.is_valid():
          data = form.save(commit=False)
          booking_id = request.POST.get('booking_id')
          print('hbhybuy',booking_id)
          price = request.POST.get('price')
          slot = Booking.objects.get(id=booking_id)
          data.slot_booking = slot.slot_booking
          
           # Generate Order Number 
          yr = int(datetime.date.today().strftime('%Y'))
          dt = int(datetime.date.today().strftime('%d'))
          mt = int(datetime.date.today().strftime('%m'))
          d = datetime.date(yr,mt,dt)
          current_date = d.strftime("%Y%m%d")
          data.save()
          order_number = current_date + str(data.id)
          data.order_number = order_number
          data.save()
          print('kjhg',data.id)
    
          return redirect('checkout',  order_id=data.id, booking_id=booking_id, price=price)
      else:
          print(form.errors)
          return HttpResponse('k')

def checkout(request,order_id,booking_id,price):
    user = request.user 

    data = get_object_or_404(OrderDetails, id=order_id)
    booking = get_object_or_404(Booking,id=booking_id)

    grant_totel = 0
    total = price 

    tax = (2 * total)/100 
    grant_totel = total + tax
    request.session['total']= total
    request.session['tax']= tax
    
    print(grant_totel)

    client = razorpay.Client(auth =(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
    payment = client.order.create({'amount':int(grant_totel)*100,'currency':'INR' , 'payment_capture':1})
    key_id = settings.RAZOR_PAY_KEY_ID
    print(payment)

    context = {
    'user':user,
    'data': data,
    'booking': booking,
    'payment': payment,
    'booking_id': booking.id,
    'order_id': order_id,
    'grand_total': grant_totel, 
    'tax': tax, 
    'price': price, 
    'order_number':data.order_number,
    }
    return render(request, 'order/checkout.html',context)

    
  
  
def success(request):
    user = request.user
    total = request.session.get('total')
    # tax = request.session.get('tax')
    # print('tax',tax)
    order_id = request.GET.get('order_id')
    booking_id = request.GET.get('booking_id')
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    
    try:
        print('hi')
        order = OrderDetails.objects.get(id = order_id)
        order.is_ordered = True
        order.user=user
        order.save()
        booking = get_object_or_404(Booking, id=booking_id)
        
    except Booking.DoesNotExist:
        return HttpResponse('jj')


    client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
    try :
        payment = client.payment.fetch(razorpay_payment_id)
        amount_paid = payment['amount'] / 100 # Amount is in paise, so convert to rupees
        razorpay_status = payment['status']
        
        print('status',razorpay_status)
        
        
        payment_detail = PaymentDetail.objects.create(
            razorpay_payment_id=razorpay_payment_id,
            user=user,  # Assuming Booking has a user field
            package=booking.package,
            booking=booking,
            amount_paid=amount_paid,
            razor_pay_status=razorpay_status
        )
        
        ordered_product = OrderProduct.objects.create(
            user=user,
            payment=payment_detail,
            order=order,
            booking=booking,
            price=amount_paid,  # Update this based on your logic
            ordered=True,
            package=booking.package
        )
        print(ordered_product.package)
        
        booking.is_paid = True
        booking.user = user
        booking.save()
        
        order.payment =payment_detail
        order.save()
        tax = ordered_product.price-total
        
        if send_invoice_email(request,user, booking, ordered_product):
                print("Email sent successfully")
        else:
                print("Failed to send email")
                

      
    except razorpay.errors.BadRequestError as e:
        return HttpResponse(f'Error: {str(e)}')
    
    context = {
        'order':order,
        'booking': booking,
        'user': booking.user,
        'ordered_product':ordered_product,
        'amount_paid': amount_paid,
        'razor_pay_status': razorpay_status,
        'order_number':order.order_number,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_order_id': razorpay_order_id,
        'tax':tax,
        'total':total
    }
    
    
    return render(request, 'order/success.html', context)


def generate_pdf(html):
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None
  

def send_invoice_email(request,user, booking, ordered_product):
    total = request.session.get('total')
    tax = request.session.get('tax')
    payment_id = PaymentDetail.objects.filter(orderdetails__order_number=ordered_product).values()
    
    print('first',payment_id[0])
    payment_id=payment_id[0]
    print('second',payment_id['razorpay_payment_id'])
    
    html = render_to_string('order/receipt_email.html', {
        'user': user,
        'booking': booking,
        'total':total,
        'tax':tax,
        'payment_id':payment_id,
        'ordered_product': ordered_product,
        'razorpay_payment_id':payment_id['razorpay_payment_id'],
    })

    pdf = generate_pdf(html)
    if pdf is None:
        return False

    mail_subject = "Your booking receipt"
    message = "Thank you for Choose US"
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]

    email = EmailMessage(mail_subject, message, from_email, to_email)
    email.attach('invoice.pdf', pdf, 'application/pdf')


    try:
        email.send()
        return True
    except Exception as e:
        print("An error occurred while sending the email:")
        print(f"Exception type: {type(e)}")
        print(f"Exception message: {e}")
        print(e)
        return False


