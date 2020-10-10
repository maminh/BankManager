import datetime
import logging

from celery.schedules import crontab
from celery.task import periodic_task

from users.models import Account

logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab(hour=00, minute=30))
def deposit_profit():
    logger.info(f'task started at {datetime.datetime.now()}')
    for account in Account.objects.filter(user__is_active=True):
        profit = None
        for i in range(10):
            try:
                profit = account.amount * 0.1
                logger.info(f'deposit profit with amount {profit} for account with id {account.id}')
                account.amount += profit
                account.save(update_fields=['amount'])
                logger.info(f'deposit successfully completed for account {account.id}')
                break
            except Exception as exc:
                logger.error(
                    f'exception {exc} for {account.id}, amount:{account.amount}, profit: {profit}, trying: {10}'
                )
        else:
            logger.error(f'unable to deposit profit for {account.id}, amount:{account.amount}, profit: {profit}')
    logger.info(f'task finished at {datetime.datetime.now()}')
