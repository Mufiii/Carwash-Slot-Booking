from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser


admin.site.register(CustomUser)