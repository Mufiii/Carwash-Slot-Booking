from django.db import models
from userview.models import CustomUser
from django.contrib.auth.models import Group
# Create your models here.


class VehicleCategory(models.Model):
    name = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name

class Package(models.Model):    
    category = models.ForeignKey(VehicleCategory,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='packages/', null=True, blank=True) 
    name = models.CharField(max_length=100, null=True,)
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
class Vehicletype(models.Model) :
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Variations(models.Model):
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(Vehicletype,on_delete=models.CASCADE)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.package


class Slot(models.Model):
    date = models.DateField(null=True, blank=True)
    available_slots = models.CharField(max_length=100)
    is_locked = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.available_slots

class SlotBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    booking_date = models.DateField(null=False)
    is_booked = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.slot} - {self.booking_date}"


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package = models.ForeignKey(Package,on_delete=models.CASCADE,default=None,null=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vehicle_no = models.CharField(max_length=50)
    variation = models.ForeignKey(Variations, on_delete=models.CASCADE, null=True,blank=True)
    slot_booking = models.ForeignKey(SlotBooking, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
        
    #     for field in self.fields :
    #         self.fields[field].widget.attrs['class'] = 'form-control'

class Userprofile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address_line = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    
    
    
  