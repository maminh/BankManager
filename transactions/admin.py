from django.contrib import admin
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from branches.models import Branch
from .models import Transaction


class TransactionResource(resources.ModelResource):
    transaction_type = fields.Field(attribute='get_transaction_type_display', column_name='transaction type')

    class Meta:
        model = Transaction
        fields = (
            'account__first_name', 'account__last_name', 'account__identity_number', 'transaction_type', 'branch__name',
            'transaction_date', 'amount', 'account__amount'
        )
        export_order = (
            'account__first_name', 'account__last_name', 'account__identity_number', 'account__amount', 'branch__name',
            'transaction_date', 'transaction_type', 'amount'
        )


@admin.register(Transaction)
class TransactionAdmin(ImportExportActionModelAdmin):
    search_fields = ('account__first_name', 'account__last_name', 'account__identity_number')
    list_display = ('amount', 'transaction_date', 'account', 'branch', 'transaction_type')
    fields = ('amount', 'transaction_date', 'account', 'branch', 'transaction_type')
    list_filter = ('branch', 'transaction_type')
    readonly_fields = ('transaction_date',)
    raw_id_fields = ('account', 'branch',)
    radio_fields = {'transaction_type': admin.HORIZONTAL}
    date_hierarchy = 'transaction_date'
    resource_class = TransactionResource

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'branch' and not request.user.is_superuser:
            kwargs['queryset'] = Branch.objects.filter(manager=request.user)
        return super(TransactionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_module_permission(self, request):
        return hasattr(request.user, 'managed_branch') or request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or (obj is None and hasattr(request.user, 'managed_branch')):
            return True
        return obj and request.user == obj.branch.manager

    def has_add_permission(self, request):
        if request.user.is_superuser or hasattr(request.user, 'managed_branch'):
            return True
        return False

    def get_queryset(self, request):
        queryset = super(TransactionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(branch=request.user.managed_branch if hasattr(request.user, 'managed_branch') else None)
