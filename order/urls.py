from django.urls import path
from .import views 


urlpatterns = [
    path('place_order/<int:id>/<int:pack_id>/',views.place_order, name="place_order"),
    path('checkout/<int:order_id>/<int:booking_id>/',views.checkout, name="checkout"),
    path('success/',views.success,name="success")
]