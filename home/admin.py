from django.contrib import admin
from .models import *

# Register your models here.

class PackageAdmin(admin.ModelAdmin):
  list_display = ('category','image','name','description')

admin.site.register(Package,PackageAdmin)

admin.site.register(VehicleCategory)
admin.site.register(SlotBooking)
admin.site.register(Vehicletype)
admin.site.register(Userprofile)



class BookingAdmin(admin.ModelAdmin):
  list_display = ('id','user','package','make','model','vehicle_no','slot_booking','is_paid','created_at','updated_at')

admin.site.register(Booking,BookingAdmin)

class VaritionsAdmin(admin.ModelAdmin):
    list_display = ('package','vehicle_type','price','is_active')
    list_editable = ('is_active',)
    list_filter = ('package','vehicle_type','price','is_active')
    

admin.site.register(Variations,VaritionsAdmin)

class SlotAdmin(admin.ModelAdmin):
  list_display = ('date','available_slots','is_locked')

admin.site.register(Slot,SlotAdmin)