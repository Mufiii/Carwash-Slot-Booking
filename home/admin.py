from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Order)
admin.site.register(payment)
admin.site.register(Customer)

class vehicleadmin(admin.ModelAdmin):
  list_display= ('customer','make','model','vehicle_type','registration_no','color')

admin.site.register(Vehicle,vehicleadmin)


