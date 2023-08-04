from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('userview.urls')),
    path('home/',include('home.urls')),
    path('cart/',include('cart.urls')),
    path('order/',include('order.urls'))
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)