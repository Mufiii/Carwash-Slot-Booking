from django.urls import path
from .import views 


urlpatterns = [
    path('packages/',views.packages,name='packages'),
    path('booking/<int:book_id>/', views.booking, name='booking'),
    
    path('dashboard/',views.dashboard, name='dashboard'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('myorders/',views.myorders, name="myorders"),
    path('order_detail/<int:order_id>/',views.order_detail, name="order_detail"),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
