from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


def validate_manager(user_id):
    user = User.objects.get(id=user_id)
    if not user.is_staff:
        raise ValidationError(_('manager should be from staff'))


class Branch(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name=_('name'))
    phone_number = PhoneNumberField(unique=True, verbose_name=_('phone number'))
    address = models.TextField(verbose_name=_('address'))
    manager = models.OneToOneField(User, verbose_name=_('manager'), on_delete=models.PROTECT,
                                   related_name='managed_branch', validators=(validate_manager,))

    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_('modified date'))

    class Meta:
        verbose_name = _('branch')
        verbose_name_plural = _('branches')

    def __str__(self):
        return self.name

    @property
    def total_deposit(self):
        return self.accounts.aggregate(models.Sum('amount'))['amount__sum']
