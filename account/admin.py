from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#we change the 'UserAdmin' to 'BaseUserAdmin' for django to did not confuse by our class in hear
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.forms import AdminPasswordChangeForm


#class UserAdmin(admin.ModelAdmin):
#    list_display = ['username', 'email']


#@admin.register(User)
class UserAdmin (BaseUserAdmin):
    fieldsets = (   #settings for admin page in person
        ('authentication:', {'fields': ('email', 'full_name', 'password')}),
        (_('Your personal info:'), {'fields': ('avatar',)}),
        (_('Your permissions:'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Your important dates:'), {'fields': ('last_login', 'date_joined')}), # 
    )
    
    add_fieldsets = (   #settings for admin page add the new person
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'avatar', 'is_superuser',
            'is_staff', 'groups', 'user_permissions','password1', 'password2'),
        }),
    )

    
    list_display = ('email', 'full_name', 'is_staff', 'is_active', 'last_login')
    #settings for admin page in group
    #show the 'username'and 'imail' in admin list
    ordering =('full_name',)
    change_password_form = AdminPasswordChangeForm


admin.site.register(User, UserAdmin)