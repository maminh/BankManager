from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.test import TestCase

from .models import User, Branch


class BranchModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = User.objects.create(email='staff@mail.com', mobile_number='+989121234567',
                                             password='foo', is_staff=True)
        cls.customer_user = User.objects.create(email='customer@mail.com',
                                                mobile_number='+989121234568', password='foo')

    def test_create_branch(self):
        branch_obj = Branch.objects.create(
            name='branch name', address='address', phone_number='+982177123456', manager=self.staff_user
        )

        self.assertEqual(Branch.objects.count(), 1)

        saved_branch = Branch.objects.first()

        self.assertEqual(saved_branch.name, branch_obj.name)
        self.assertEqual(saved_branch.address, branch_obj.address)
        self.assertEqual(saved_branch.phone_number, branch_obj.phone_number)
        self.assertEqual(saved_branch.manager, branch_obj.manager)

    def test_delete_manager(self):
        branch_obj = Branch.objects.create(
            name='branch name', address='address', phone_number='+982177123456', manager=self.staff_user
        )

        with self.assertRaises(ProtectedError):
            self.staff_user.delete()

        another_manager = User.objects.create(email='staff2@mail.com', mobile_number='+989121234569',
                                              password='foo', is_staff=True)
        branch_obj.manager = another_manager
        branch_obj.save()
        self.staff_user.delete()
        self.assertEqual(branch_obj.manager, another_manager)

    def test_invalid_manager(self):
        branch_obj = Branch(
            name='branch name', address='address', phone_number='+982177123456', manager=self.customer_user
        )
        with self.assertRaises(ValidationError):
            branch_obj.full_clean()
