from django.contrib import admin
from .models import *

# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
  list_display = ('id','razorpay_payment_id','package','booking','user','amount_paid','created_at')
  
admin.site.register(PaymentDetail,PaymentAdmin)


class OrderAdmin(admin.ModelAdmin):
   list_display = ('id','payment','order_number','is_ordered')
  
admin.site.register(OrderDetails,OrderAdmin)


admin.site.register(OrderProduct)