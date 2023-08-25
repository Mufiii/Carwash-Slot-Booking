from datetime import datetime, timedelta, timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import razorpay
from django.utils import timezone
from CarWash import settings
from .forms import *
from .models import *
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib import messages
from order.forms import *
from userview.views import delete_booking
from django.db.models import Count


@login_required
def dashboard(request) :
    user = request.user
    orders = OrderProduct.objects.order_by('-created_at').filter(user=user,order__is_canceled=False)
    order_count = orders.count()
    context = { 
        'order_count':order_count,
        'user': user
    }
    return render(request,'home/dashboard.html',context)

      

def packages(request):
    print(request,"sdfghjkl")
    packages = Package.objects.all()
    delete_booking(request)
    try:
        price = 0
        value = request.POST.get('category')
          
        if value == 'car':
            packages = Package.objects.filter(category__name='CAR')
            return render(request, 'home/packages.html', {'packages': packages, 'price': price})
        elif value == 'bike':
            packages = Package.objects.filter(category__name='BIKE')
            return render(request, 'home/packages.html', {'packages': packages, 'price': price})
        else :
            pass
    except Exception as e:
        pass
    context = {
    'packages': packages, 
    'price': price,
    # 'variation':variation
    }
    return render(request, 'home/packages.html', context)




    
def booking(request, book_id):
    booked_slots = SlotBooking.objects.all().values('slot__available_slots','booking_date')
    print('booked_slots: ',booked_slots)
    user = request.user
    package = Package.objects.get(id=book_id)
    price=0
    morning_slot = Slot.objects.filter(groups__name='morning')
    afternoon_slot = Slot.objects.filter(groups__name='afternoon')
    evening_slot = Slot.objects.filter(groups__name='evening')
    
    current_date = datetime.now().date()
    
    five_days_later = current_date + timedelta(days=4)
    date_list = []
    while current_date <= five_days_later:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    if request.method == 'POST':
        print(request.POST)
        form = BookingForm(request.POST)
        if form.is_valid():
            selected_date = request.POST.get('selected_date')
            selected_slot_id = request.POST.get('selected_slot')
            slot_instance = get_object_or_404(Slot, pk=selected_slot_id)
            price=request.POST.get('price')
            
            slot_booking, created = SlotBooking.objects.get_or_create(
                user=request.user,
                slot=slot_instance,
                booking_date=selected_date
            )
            slot_booking.save()
            print(slot_booking)
            
            if not slot_booking.is_booked:
                # Proceed with booking
                booking = Booking.objects.create(
                    user=slot_booking.user,  # Associate the booking with the logged-in user
                    make=form.cleaned_data['make'],
                    model=form.cleaned_data['model'],
                    vehicle_no=form.cleaned_data['vehicle_no'],
                    slot_booking=slot_booking,
                    package = package       
                )
                # Mark the slot as booked
                slot_booking.is_booked = True
                slot_booking.save()
                context= {
                        'order':Booking.objects.get(id = booking.id,),
                        'form' : OrderForm(),
                        'packages':Package.objects.get(pk=package.id),
                        'price':price,
                }
                return render(request, 'order/place_order.html',context)
                
            else:
                # The slot is already booked for the selected date
                form.add_error('start_date', 'The selected slot is not available for booking.')
        else:
            # Handle the case when the selected_date is None or empty
            form.add_error('start_date', 'Please select a valid date.')
    
    else:
        form = BookingForm()
        form.fields['start_date'].widget.attrs['min'] = current_date
        form.fields['start_date'].widget.attrs['max'] = five_days_later
        price=request.GET.get('price')
        

    context = {
        'booked_slots':booked_slots,
        'package': package,
        'user': request.user,
        'form': form,
        'morning_slot': morning_slot,
        'afternoon_slot': afternoon_slot,
        'evening_slot': evening_slot,
        'date_list': date_list,
        'price':price,
    }
    return render(request, 'home/booking.html',context)



@login_required(login_url='login')
def myorders(request) :
    orders = OrderDetails.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context ={
        'orders':orders
    }
    return render(request,'home/myorders.html',context)



def order_detail(request,order_id):
    print(order_id)
    order_detail = OrderProduct.objects.get(order__order_number=order_id)
    order = OrderDetails.objects.get(order_number=order_id)
   
    context = {
        'order_detail':order_detail,
        'order':order,
    }
    return render(request,'home/order_detail.html',context)


def cancel_order(request, order_id):
    print(order_id)
    order = get_object_or_404(OrderDetails, id=order_id)
    
    # booking_time = order.slot_booking.slot
    # print(booking_time)
    # current_time = datetime.now()
    # print(current_time)
    # time_difference = booking_time - current_time
    # print(time_difference)
    
    if request.method == 'POST':
        order.is_canceled = True
        order.save()
        c = SlotBooking.objects.get(id=order.slot_booking.id)
        c.is_booked = False
        c.save()
        messages.success(request, 'Your Order is Cancelled Successfully')
    
    
        return redirect('myorders')
        
    context = {
        'order': order,
    }
    return render(request, 'home/myorders.html', context)


        
        # client = razorpay.Client(auth =(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
        
        # payment_id = order.payment_id
        # print(payment_id)
        # refund_amount = order.payment.amount_paid
        # print(refund_amount)
        
        # refund_data = {
        #     "amount": refund_amount * 100,  # Razorpay expects amount in paise
        #     "speed": "normal",  # Or "immediate" for instant refund
        #     "receipt": f"refund_{payment_id}",  # Unique receipt for the refund
        #     "note": "Refund for canceled order",
        #     # You might need additional fields like UPI ID to process the refund
        # }
        # try:
        #     refund = client.payment.refund(payment_id, refund_data)
        #     # Process the refund response and update your database if needed
        #     refund_status = refund.get('status')  # Check if the refund was successful
        #     if refund_status == 'processed':
        #         # Update your order or refund status accordingly
        #         order.refund_status = 'processed'
        #         order.save()
        #         messages.success(request, 'Refund processed successfully')
        #     else:
        #         messages.error(request, 'Refund processing failed')
        # except RazorpayError as e:
        #     messages.error(request, 'An error occurred during refund processing')

        # order.slot_booking.is_booked=False
        
    
    



@login_required(login_url='login')
def edit_profile(request):
    userprofile, created = Userprofile.objects.get_or_create(user=request.user)

    if request.method == 'POST' :
        user_form = UserForm(request.POST, instance = request.user)
        user_profile = UserProfileForm(request.POST, instance = userprofile)
        if user_form.is_valid() and user_profile.is_valid():
            user_form.save()
            user_profile.save()
            messages.success(request, 'Your Profile has been Updated') 
            return redirect('edit_profile')
    else :
        user_form = UserForm(instance=request.user)
        user_profile = UserProfileForm(instance=userprofile)
        
    context = {
        'user_form':user_form,
        'user_profile':user_profile
    }
    return render(request, 'home/edit_profile.html',context)



@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user = CustomUser.objects.get(username__exact= request.user.username)
        
        if new_password == confirm_password :
            success = user.check_password(current_password)
            if success :
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request,'Password updated Successfully')
                return redirect('change_password')
            else :
                messages.error(request,'Enter Valid Current Password')
                return redirect('change_password')
        else :
            messages.error(request,'Password does not match')
            return redirect('change_password')
    return render(request, 'home/change_password.html')



    