from django.urls import path
from .import views 


urlpatterns = [
    path('place_order/',views.place_order, name="place_order"),
    path('checkout/<int:order_id>/<int:booking_id>/<int:price>/',views.checkout, name="checkout"),
    path('success/', views.success, name='success'),
    
]