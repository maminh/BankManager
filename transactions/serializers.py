import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework import serializers

from .models import Transaction
from .tasks import send_sms

logger = logging.getLogger(__name__)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'branch', 'transaction_type', 'transaction_date')
        read_only_fields = ('transaction_date',)

    def get_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user

    def validate(self, attrs):
        user = self.get_user()
        attrs['account'] = user.account

        if attrs['transaction_type'] == Transaction.TRANSACTION_WITHDRAW and attrs['amount'] > user.account.amount:
            raise serializers.ValidationError(_('account deposit is not enough for this transaction'))

        return attrs

    def create(self, validated_data):
        account = self.get_user().account
        if validated_data['transaction_type'] == Transaction.TRANSACTION_WITHDRAW:
            account.amount -= validated_data['amount']
        else:
            account.amount += validated_data['amount']
        try:
            with transaction.atomic():
                ret = super(TransactionSerializer, self).create(validated_data)
                account.save(update_fields=['amount'])
                send_sms.delay(ret.id, account.id)
        except Exception as exc:
            logger.error(f'{exc} happened when creating transaction {validated_data} for account {account}')
            raise exceptions.APIException('unable to submit exception')
        logger.info(f'transaction {ret.id} successfully created for account {account.id}')
        return ret
