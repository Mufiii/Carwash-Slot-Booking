from django.db import models
from userview.models import CustomUser

# Create your models here.

class Order(models.Model) :
  STATUS = (
      ('Bike','Bike'),
      ('Car','Car'),
    ) 
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE )
  order_number = models.CharField(max_length=100)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  phone = models.CharField(max_length=15)
  email = models.EmailField(unique=True)
  address = models.CharField(max_length=50)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  country = models.CharField(max_length=50)
  order_note = models.TextField(max_length=100 , blank=True)  
  make = models.CharField(max_length=100)
  model = models.CharField(max_length=100)
  registration_no = models.CharField(max_length=50)
  color = models.CharField(max_length=50)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  category = models.CharField(max_length=255, choices=STATUS)
  is_ordered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True) 
  
  def __str__(self):
      return self.first_name

  


 



  
  
  