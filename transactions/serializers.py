from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Transaction


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

    @transaction.atomic
    def create(self, validated_data):
        account = self.get_user().account
        ret = super(TransactionSerializer, self).create(validated_data)
        if validated_data['transaction_type'] == Transaction.TRANSACTION_WITHDRAW:
            account.amount -= validated_data['amount']
        else:
            account.amount += validated_data['amount']
        account.save(update_fields=['amount'])
        return ret
