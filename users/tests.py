from django.db.transaction import TransactionManagementError
from django.db.utils import IntegrityError
from django.test import TestCase

from branches.models import Branch
from .models import Account, CustomUser
from .tasks import deposit_profit


class UsersManagersTests(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(email='normal@user.com', password='foo')

        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(email='normal@user.com')
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(email='')
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        admin_user = CustomUser.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(email='super@user.com', password='foo', is_superuser=False)


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(email='normal@user.com', password='foo')
        manager = CustomUser.objects.create_superuser('super@user.com', 'foo')
        cls.branch = Branch.objects.create(
            name='test branch', address='address', phone_number='+982177123456', manager=manager
        )

    def test_create_account(self):
        account = Account.objects.create(first_name='amin', last_name='hosseini', user=self.user,
                                         mobile_number='+989121234567', branch=self.branch)
        self.assertEqual(1, Account.objects.count())

        saved_account = Account.objects.first()

        self.assertEqual(account.first_name, saved_account.first_name)
        self.assertEqual(account.last_name, saved_account.last_name)
        self.assertEqual(account.user, saved_account.user)
        self.assertEqual(account.mobile_number, saved_account.mobile_number)
        self.assertEqual(account.branch, saved_account.branch)

    def test_duplicate_account(self):
        account = Account.objects.create(first_name='amin', last_name='hosseini', user=self.user,
                                         mobile_number='+989121234567', branch=self.branch,
                                         identity_number='0011234567')

        with self.assertRaises(IntegrityError):
            Account.objects.create(first_name='amin', last_name='hosseini', user=self.user,
                                   mobile_number='+989121234568', branch=self.branch,
                                   identity_number='0011234567')

        with self.assertRaises(TransactionManagementError):
            Account.objects.create(first_name='amin', last_name='hosseini', user=self.user,
                                   mobile_number='+989121234567', branch=self.branch,
                                   identity_number='0011234568')


class UsersTaskTest(TestCase):
    def setUp(self) -> None:
        self.user_a = CustomUser.objects.create(email='user1@mail.com', password='foo')
        self.user_b = CustomUser.objects.create(email='user2@mail.com', password='foo')
        self.user_inactive = CustomUser.objects.create(email='user3@mail.com', password='foo', is_active=False)
        user_manager = CustomUser.objects.create(email='manager@mail.com', password='foo', is_staff=True)

        branch = Branch.objects.create(
            name='test branch', address='address', phone_number='+982177123456', manager=user_manager
        )

        self.account_a = Account.objects.create(first_name='amin', last_name='hosseini', user=self.user_a,
                                                mobile_number='+989121234568', branch=branch,
                                                identity_number='0011234567', amount=100)
        self.account_b = Account.objects.create(first_name='amin', last_name='hosseini', user=self.user_b,
                                                mobile_number='+989121234569', branch=branch,
                                                identity_number='0011234569', amount=15)
        self.account_inactive = Account.objects.create(first_name='amin', last_name='hosseini', user=self.user_inactive,
                                                       mobile_number='+989121234567', branch=branch,
                                                       identity_number='0011234564', amount=20)

    def test_task(self):
        deposit_profit.apply()
        self.assertEqual(Account.objects.get(id=self.account_a.id).amount, 110)
        self.assertEqual(Account.objects.get(id=self.account_b.id).amount, 16.5)
        self.assertEqual(Account.objects.get(id=self.account_inactive.id).amount, 20)
