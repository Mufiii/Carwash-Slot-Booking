from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

     
            
#             # Generate Order Number 
#             # yr = int(datetime.date.today().strftime('%Y'))
#             # dt = int(datetime.date.today().strftime('%d'))
#             # mt = int(datetime.date.today().strftime('%m'))
#             # d = datetime.date(yr,mt,dt)
#             # current_date = d.strftime("%Y%m%d")
#             # order_number = current_date + str(order.id)
#             # order.order_number = order_number
          
            
#             order_number = f"{datetime.date.today().strftime('%Y%m%d')}{order.id}"
#             order.order_number = order_number
#             order.save()




def myorders(request) :
    return render(request,'home/order_success.html')


@login_required
def dashboard(request) :
    # orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    # order_count = orders.count()
    user = request.user
    context = {
        'user': user
    }
    return render(request,'home/dashboard.html',context)

      
def packages(request): 
    if request.method == 'POST':
            print(request.POST)
            value = request.POST.get('package')
            print(value)
            if value == 'reguler':
                packages = CarWashPackage.objects.filter(vehicle_type=1)
                print(packages)
                return render(request, 'home/packages.html', {'packages': packages})
            elif value == 'medium':
                packages = CarWashPackage.objects.filter(vehicle_type=2)
                return render(request, 'home/packages.html', {'packages': packages})
            elif value == 'compact':
                packages = CarWashPackage.objects.filter(vehicle_type=3)
                return render(request, 'home/packages.html', {'packages': packages})
            elif value == 'sports':
                packages = CarWashPackage.objects.filter(vehicle_type=4)
                return render(request, 'home/packages.html', {'packages': packages})
    return render(request, 'home/packages.html')



def booking(request, book_id):
    book = CarWashPackage.objects.get(id=book_id)

    morning_slot = Slot.objects.filter(groups=4)
    afternoon_slot = Slot.objects.filter(groups=6)
    evening_slot = Slot.objects.filter(groups=5)

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
            print(selected_date)
            print(type(selected_date))
            print('hg')
            slot_instance = get_object_or_404(Slot, pk=selected_slot_id)

            # Check if the slot is available for the selected date
            # if selected_date is not None and selected_date != '':
            slot_booking, created = SlotBooking.objects.get_or_create(
                slot=slot_instance,
                booking_date=selected_date
            )
            # print("booking",booking_date)
            
            if not slot_booking.is_booked:
                # Proceed with booking
                booking = Booking.objects.create(
                    user=request.user,  # Associate the booking with the logged-in user
                    make=form.cleaned_data['make'],
                    model=form.cleaned_data['model'],
                    vehicle_no=form.cleaned_data['vehicle_no'],
                    slot_booking=slot_booking,
                    package = book
                    
                )
                print('jh')
                # Mark the slot as booked
                slot_booking.is_booked = True
                slot_booking.save()

                return redirect('place_order', id=booking.id,pack_id=book.id)
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

    context = {
        'book': book,
        'user': request.user,
        'form': form,
        'morning_slot': morning_slot,
        'afternoon_slot': afternoon_slot,
        'evening_slot': evening_slot,
        'date_list': date_list,
    }
    return render(request, 'home/booking.html', context)












