from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser


class customuseradmin(admin.ModelAdmin) :
  list_display = ('first_name','last_name','email','phone','is_active')

admin.site.register(CustomUser,customuseradmin)