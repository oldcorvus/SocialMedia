from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'username']


admin.site.register(CustomUser)
