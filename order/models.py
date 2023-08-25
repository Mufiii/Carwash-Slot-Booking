from django.db import models
from userview.models import *
from home.models import *

class PaymentDetail(models.Model) :
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    amount_paid = models.CharField(max_length=100) # this is the total amount
    razor_pay_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)

    

class OrderDetails(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
  payment = models.ForeignKey(PaymentDetail, on_delete=models.CASCADE, null=True)
  slot_booking = models.ForeignKey(SlotBooking, on_delete=models.CASCADE,null=True)
  order_number = models.CharField(max_length=100)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  phone = models.CharField(max_length=100)
  email = models.EmailField(max_length=100)
  address = models.CharField(max_length=100)
  street = models.CharField(max_length=100)
  building = models.CharField(max_length=100)
  zip = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  country = models.CharField(max_length=100)
  is_ordered = models.BooleanField(default=False)
  is_canceled = models.BooleanField(default=False)
  order_note = models.TextField(max_length=200,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.first_name
  
  def full_name(self):
    return f"{self.first_name} {self.last_name}"
  
  
class OrderProduct(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
  payment = models.ForeignKey(PaymentDetail, on_delete=models.CASCADE, null=True,blank=True)
  order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE, null=True)
  booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
  package = models.ForeignKey(Package,on_delete=models.CASCADE, null=True)
  variations = models.ManyToManyField(Variations,blank=True)
  price = models.FloatField()
  ordered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.order.order_number
  
  
