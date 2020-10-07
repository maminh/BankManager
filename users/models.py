from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_('modified date'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Account(models.Model):
    mobile_number = PhoneNumberField(verbose_name=_('phone number'), unique=True)
    identity_number = models.CharField(verbose_name=_('identity'), max_length=11, unique=True)

    first_name = models.CharField(verbose_name=_('first name'), max_length=64)
    last_name = models.CharField(verbose_name=_('last name'), max_length=64)

    amount = models.PositiveIntegerField(verbose_name=_('amount'), default=0)

    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_('modified date'))

    branch = models.ForeignKey(
        'branches.Branch', verbose_name=_('created branch'), related_name='accounts', on_delete=models.PROTECT
    )

    user = models.OneToOneField(
        CustomUser, verbose_name=_('associated user'), related_name='account', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.identity_number}'
