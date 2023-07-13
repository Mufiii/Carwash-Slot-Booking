from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Order)
admin.site.register(Vehicle)
admin.site.register(Category)
admin.site.register(Slot)