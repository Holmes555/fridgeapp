from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from sunflower.forms import CustomUserChangeForm, CustomUserCreationForm
from sunflower.models.user import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email']


admin.site.register(CustomUser, CustomUserAdmin)
