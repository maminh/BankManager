from django.contrib import admin

from .models import Branch, User


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'manager', 'created_date', 'modified_date', 'total_deposit')
    fields = ('name', ('phone_number', 'address'), 'manager', ('created_date', 'modified_date'), 'total_deposit')
    readonly_fields = ('created_date', 'modified_date', 'total_deposit')
    search_fields = ('name', 'address')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'manager':
            kwargs['queryset'] = User.objects.filter(is_staff=True, is_superuser=False)
        return super(BranchAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_module_permission(self, request):
        return hasattr(request.user, 'managed_branch') or request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or (obj is None and hasattr(request.user, 'managed_branch')):
            return True
        return obj and request.user == obj.manager

    def get_queryset(self, request):
        queryset = super(BranchAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(manager=request.user)
