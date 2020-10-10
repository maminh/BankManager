import logging

from celery import shared_task

from transactions.models import Transaction
from users.models import Account

logger = logging.getLogger(__name__)


@shared_task
def send_sms(transaction_id, account_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        account = Account.objects.get(id=account_id)
    except Transaction.DoesNotExist:
        logger.error(f'transaction with id {transaction_id} does not existed')
        return
    except Account.DoesNotExist:
        logger.error(f'account with id {account_id} does not existed')
        return
    text = f"Dear {account.first_name}\n" \
           f"{transaction.get_transaction_type_display()} with amount {transaction.amount} completed \n" \
           f"date: {transaction.transaction_date}\n" \
           f"current deposit: {account.amount}"
    # SMPP Server api will call here
    logger.info(f'sending:\n"{text}"\nto {account.mobile_number}')
    return text
