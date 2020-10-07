from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Account


class AccountInLine(admin.StackedInline):
    extra = 1
    model = Account
    fields = (('first_name', 'last_name'), 'identity_number', 'mobile_number', 'branch', 'amount', 'user',
              ('created_date', 'modified_date'))
    readonly_fields = ('created_date', 'modified_date', 'amount')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'created_date', 'modified_date')
    list_filter = ('is_staff', 'is_active',)
    date_hierarchy = 'created_date'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (AccountInLine,)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'identity_number', 'mobile_number', 'branch', 'amount', 'user',)
    fields = (('first_name', 'last_name'), 'identity_number', 'mobile_number', 'branch', 'amount', 'user',
              ('created_date', 'modified_date'))
    readonly_fields = ('created_date', 'modified_date', 'amount')
    search_fields = ('identity_number', 'mobile_number', 'first_name', 'last_name')
    list_filter = ('branch',)
    raw_id_fields = ('branch', 'user')
