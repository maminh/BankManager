from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'mobile_number', 'is_staff', 'is_active', 'created_date', 'modified_date')
    list_filter = ('email', 'mobile_number', 'is_staff', 'is_active',)
    date_hierarchy = 'created_date'
    fieldsets = (
        (None, {'fields': ('email', 'mobile_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile_number', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'mobile_number')
    ordering = ('email',)
