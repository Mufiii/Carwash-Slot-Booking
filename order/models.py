from django.db import models
from home.models import Booking, CarWashPackage
from userview.models import *

class PaymentDetail(models.Model) :
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    package = models.ForeignKey(CarWashPackage,on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    amount_paid = models.CharField(max_length=100) # this is the total amount
    razor_pay_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.razor_payment_id)

    

class OrderDetails(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
  order_number = models.CharField(max_length=100)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  phone = models.CharField(max_length=100)
  email = models.EmailField(max_length=100)
  address = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  country = models.CharField(max_length=100)
  order_note = models.TextField(max_length=200,blank=True)
  is_paid = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.first_name