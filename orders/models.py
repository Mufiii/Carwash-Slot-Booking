from django.db import models
from userview.models import CustomUser

# Create your models here.

class Category(models.Model):
    STATUS = (
      ('Bike','Bike'),
      ('Car','Car'),
    ) 
    name = models.CharField(max_length=255, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
      

class Vehicle(models.Model) :
  
  make = models.CharField(max_length=100)
  model = models.CharField(max_length=100)
  registration_no = models.CharField(max_length=50)
  color = models.CharField(max_length=50)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True) 
  
  
class Slot(models.Model) :
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f'Slot {self.id}: {self.start_time} - {self.end_time}'
  

class Order(models.Model) :
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE )
  slot = models.ForeignKey( Slot, on_delete=models.CASCADE)
  vehicle = models.ForeignKey( Vehicle, on_delete=models.CASCADE)
  category = models.ForeignKey( Category , on_delete=models.CASCADE, null=True, default=None)
  order_number = models.CharField(max_length=100)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  phone = models.CharField(max_length=15)
  email = models.EmailField(unique=True)
  address = models.CharField(max_length=50)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  country = models.CharField(max_length=50)
  Zip_Code = models.CharField(max_length=10)
  order_note = models.TextField(max_length=100 , blank=True)
  is_ordered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True) 
  
  def __str__(self):
      return self.first_name

   


 



  
  
  