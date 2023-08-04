from django.db import models
from userview.models import CustomUser
from django.contrib.auth.models import Group
# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name

class CarWashPackage(models.Model):
    image = models.ImageField(upload_to='packages_images/', null=True, blank=True) 
    name = models.CharField(max_length=100, null=True,)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    
   
    
    def __str__(self):
        return self.name


    
class Slot(models.Model):
    date = models.DateField(null=True, blank=True)
    available_slots = models.CharField(max_length=100)
    is_locked = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.available_slots

class SlotBooking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    booking_date = models.DateField(null=False)
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.slot} - {self.booking_date}"

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package = models.ForeignKey(CarWashPackage,on_delete=models.CASCADE,default=None,null=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vehicle_no = models.CharField(max_length=50)
    slot_booking = models.ForeignKey(SlotBooking, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
  