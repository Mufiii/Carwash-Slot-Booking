from django.db import models
from userview.models import CustomUser

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    
    def __str__(self):
        return self.first_name

    
class payment(models.Model) :
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=50)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    


class Vehicle(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    registration_no = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    
    def __str__(self) :
        return self.make

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(payment, on_delete=models.SET_NULL,blank=True,null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.CharField(max_length=255)
    order_note = models.TextField(max_length=100, blank=True)
    order_totel = models.FloatField()

    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

  


 



  
  
  