from django.db.transaction import TransactionManagementError
from django.db.utils import IntegrityError
from django.test import TestCase

from branches.models import Branch
from .models import Account, CustomUser


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
