from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(OrderDetails)

class PaymentAdmin(admin.ModelAdmin):
  list_display = ('id','razorpay_payment_id','package','booking','user','amount_paid',)
  
admin.site.register(PaymentDetail,PaymentAdmin)

