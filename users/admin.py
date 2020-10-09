from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Account


class AccountInLine(admin.StackedInline):
    extra = 0
    model = Account
    fields = (('first_name', 'last_name'), 'identity_number', 'mobile_number', 'branch', 'amount', 'user',
              ('created_date', 'modified_date'))
    readonly_fields = ('created_date', 'modified_date', 'amount')


class MoreAmountFilter(admin.SimpleListFilter):
    title = _('amount bigger than')
    parameter_name = 'more_amount'

    def lookups(self, request, model_admin):
        return [(1000000, _('1 million')), (10000000, _('10 million')), (100000000, _('100 million'))]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(amount__gte=int(self.value()))


class LessAmountFilter(MoreAmountFilter):
    title = _('amount less than')
    parameter_name = 'less_amount'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(amount__lte=int(self.value()))


class ZeroAmountFilter(admin.SimpleListFilter):
    title = _('zero amount accounts')
    parameter_name = 'is_zero'

    def lookups(self, request, model_admin):
        return [(True, _('zero amount accounts')), (False, _('non-zero amount accounts'))]

    def queryset(self, request, queryset):
        if self.value() is None:
            return
        if self.value().lower() == 'true':
            return queryset.filter(amount__exact=0)
        else:
            return queryset.filter(amount__gt=0)


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
    list_filter = ('user__is_active', 'branch', MoreAmountFilter, ZeroAmountFilter, LessAmountFilter)
    raw_id_fields = ('branch', 'user')

    def has_module_permission(self, request):
        return hasattr(request.user, 'managed_branch') or request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or (obj is None and hasattr(request.user, 'managed_branch')):
            return True
        return obj and request.user == obj.branch.manager

    def has_delete_permission(self, request, obj=None):
        return self.has_view_permission(request, obj)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(AccountAdmin, self).get_queryset(request)
        if hasattr(request.user, 'managed_branch'):
            return Account.objects.filter(branch=request.user.managed_branch)
