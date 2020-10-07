from django.contrib import admin

from .models import Branch, User


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'manager', 'created_date', 'modified_date')
    fields = ('name', ('phone_number', 'address'), 'manager', ('created_date', 'modified_date'))
    readonly_fields = ('created_date', 'modified_date')
    search_fields = ('name', 'address')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'manager':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super(BranchAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
