from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CarWashPackage)
admin.site.register(VehicleType)
admin.site.register(SlotBooking)


class BookingAdmin(admin.ModelAdmin):
  list_display = ('id','user','package','make','model','vehicle_no','slot_booking','is_paid','created_at','updated_at')

admin.site.register(Booking,BookingAdmin)

class SlotAdmin(admin.ModelAdmin):
  list_display = ('date','available_slots','is_locked')

admin.site.register(Slot,SlotAdmin)