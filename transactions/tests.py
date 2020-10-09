from json import loads

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from branches.models import Branch
from users.models import Account
from .models import Transaction


class TransactionTest(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        branch_manager = User.objects.create(email='manager@mail.com', password='foo', is_staff=True)
        self.branch = Branch.objects.create(name='branch test', phone_number='+982177123456', manager=branch_manager)

        self.user = User.objects.create(email='user@mail.com', password='foo')
        self.user_account = Account.objects.create(user=self.user, mobile_number='+989111234567', amount=8,
                                                   identity_number='0011234567', branch=self.branch,
                                                   first_name='amin', last_name='hosseini')
        Transaction.objects.create(branch=self.branch, account=self.user_account, amount=5,
                                   transaction_type=Transaction.TRANSACTION_WITHDRAW)
        Transaction.objects.create(branch=self.branch, account=self.user_account, amount=5,
                                   transaction_type=Transaction.TRANSACTION_WITHDRAW)
        Transaction.objects.create(branch=self.branch, account=self.user_account, amount=5,
                                   transaction_type=Transaction.TRANSACTION_WITHDRAW)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_unauthorized(self):
        self.client.force_authenticate(user=None)
        request = self.client.get(reverse('transaction-list'))
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_transactions(self):
        request = self.client.get(reverse('transaction-list'))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        content = loads(request.content)
        self.assertEqual(content.get('count'), 3)

    def test_low_withdraw_transaction(self):
        request = self.client.post(reverse('transaction-list'),
                                   {'amount': 12, 'branch': self.branch,
                                    'transaction_type': Transaction.TRANSACTION_WITHDRAW})
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_withdraw_transaction(self):
        request = self.client.post(reverse('transaction-list'),
                                   {'amount': 5, 'branch': self.branch.id,
                                    'transaction_type': Transaction.TRANSACTION_WITHDRAW})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        transaction_object = Transaction.objects.last()

        self.assertEqual(transaction_object.amount, 5)
        self.assertEqual(transaction_object.transaction_type, Transaction.TRANSACTION_WITHDRAW)
        self.assertEqual(transaction_object.branch, self.branch)
        self.assertEqual(transaction_object.account, self.user_account)
        self.assertEqual(Account.objects.get(user=self.user).amount, 3)

    def test_deposit_transaction(self):
        request = self.client.post(reverse('transaction-list'),
                                   {'amount': 12, 'branch': self.branch.id,
                                    'transaction_type': Transaction.TRANSACTION_DEPOSIT})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        transaction_object = Transaction.objects.last()

        self.assertEqual(transaction_object.transaction_type, Transaction.TRANSACTION_DEPOSIT)
        self.assertEqual(transaction_object.amount, 12)
        self.assertEqual(transaction_object.branch, self.branch)
        self.assertEqual(transaction_object.account, self.user_account)
        self.assertEqual(Account.objects.get(user=self.user).amount, 20)

    def test_non_account_user(self):
        User = get_user_model()
        branch_manager = User.objects.create(email='another@mail.com', password='foo')
        self.client.force_authenticate(user=branch_manager)

        request = self.client.get(reverse('transaction-list'))
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
