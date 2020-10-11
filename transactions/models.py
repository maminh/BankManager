from django.db import models
from django.utils.translation import gettext_lazy as _

from branches.models import Branch
from users.models import Account


class Transaction(models.Model):
    TRANSACTION_WITHDRAW = 1
    TRANSACTION_DEPOSIT = 2
    TRANSACTION_CHOICES = (
        (TRANSACTION_WITHDRAW, _('withdraw')),
        (TRANSACTION_DEPOSIT, _('deposit'))
    )

    amount = models.PositiveIntegerField(verbose_name=_('amount'))
    transaction_date = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    account = models.ForeignKey(Account, verbose_name=_('account'), related_name='transactions',
                                on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, verbose_name=_('branch'), related_name='withdraws', on_delete=models.CASCADE)
    transaction_type = models.PositiveSmallIntegerField(verbose_name=_('type'), choices=TRANSACTION_CHOICES)

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')

    def __str__(self):
        return f'{self.transaction_type}:{self.account}:{self.amount}'
