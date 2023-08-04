from django.urls import path
from .import views 


urlpatterns = [
    path('order-success/',views.myorders, name="myorders"),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('packages/',views.packages,name='packages'),
    path('booking/<int:book_id>/',views.booking,name='booking'),
    
]
