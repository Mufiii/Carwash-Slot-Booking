
from django.urls import path 
from .import views

urlpatterns = [
    path('register/',views.register , name="register"),
    path('login/',views.user_login , name='login'),
    path('forgot_password/',views.forgot_password , name="forgot"),
    path('reset-password/<int:user_id>/',views.reset_password , name="reset"),
    path('login-with-otp/',views.login_with_otp, name="login_with_otp"),
    path('verify-otp/<int:user_id>/<str:verification>/',views.verify_otp , name='verify_otp'),
    path('verify-forgot-otp/<int:user_id>/<str:verification>/',views.verify_otp , name="verify_forgot_otp"),
    path('verify-login-otp/<int:user_id>/<str:verification>/',views.verify_otp , name="verify_login_otp"),
    path('', views.home , name='home'),
    path('logout', views.logout_view,name='logout'),
    path('delete_booking', views.delete_booking,name='delete_booking'),
    
    
]
