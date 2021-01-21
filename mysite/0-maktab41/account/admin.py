from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name']

admin.site.register(User, UserAdmin)