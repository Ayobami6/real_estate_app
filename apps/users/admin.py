from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "id"]

admin.site.register(CustomUser, CustomUserAdmin)
