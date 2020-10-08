from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.test import TestCase, RequestFactory
from django.urls import reverse

from .admin import BranchAdmin
from .models import User, Branch


class BranchModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = User.objects.create(email='staff@mail.com', password='foo', is_staff=True)
        cls.customer_user = User.objects.create(email='customer@mail.com', password='foo')

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

        another_manager = User.objects.create(email='staff2@mail.com', password='foo', is_staff=True)
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


class BranchAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manager_user = User.objects.create(email='manager@mail.com', password='foo', is_staff=True)
        cls.super_user = User.objects.create_superuser(email='sudo@mail.com', password='foo', is_staff=True)
        cls.another_manager_user = User.objects.create(email='manager2@mail.com', password='foo', is_staff=True)
        cls.normal_staff_user = User.objects.create(email='staff@mail.com', password='foo', is_staff=True)
        cls.normal_user = User.objects.create(email='normal@mail.com', password='foo', is_staff=False)
        cls.branch = Branch.objects.create(
            name='branch name', address='address', phone_number='+982177123456', manager=cls.manager_user
        )
        cls.second_branch = Branch.objects.create(
            name='branch name2', address='address2', phone_number='+982177123476', manager=cls.another_manager_user
        )

    def setUp(self) -> None:
        self.site = AdminSite()
        self.model_admin = BranchAdmin(Branch, self.site)
        self.request_factory = RequestFactory()

    def test_has_module_permission(self):
        request = self.request_factory.get(reverse('admin:branches_branch_changelist'))
        request.user = self.manager_user
        self.assertTrue(self.model_admin.has_module_permission(request))

    def test_deny_has_module_permission(self):
        request = self.request_factory.get(reverse('admin:branches_branch_changelist'))
        request.user = self.normal_staff_user
        self.assertFalse(self.model_admin.has_module_permission(request))

    def test_has_view_permission(self):
        request = self.request_factory.get(reverse('admin:branches_branch_change', args=[self.branch.id]))
        request.user = self.manager_user

        self.assertTrue(self.model_admin.has_view_permission(request, self.branch))
        self.assertTrue(self.model_admin.has_view_permission(request))

    def test_deny_has_view_permission(self):
        request = self.request_factory.get(reverse('admin:branches_branch_change', args=[self.branch.id]))
        request.user = self.another_manager_user

        self.assertFalse(self.model_admin.has_view_permission(request, self.branch))

    def test_normal_staff_has_view_permission(self):
        request = self.request_factory.get(reverse('admin:branches_branch_change', args=[self.branch.id]))
        request.user = self.normal_staff_user

        self.assertFalse(self.model_admin.has_view_permission(request))
        self.assertFalse(self.model_admin.has_view_permission(request, self.branch))

    def test_queryset(self):
        request = self.request_factory.get(reverse('admin:branches_branch_changelist'))
        request.user = self.manager_user
        self.assertEqual(self.model_admin.get_queryset(request).count(), 1)
        self.assertEqual(self.model_admin.get_queryset(request).first(), self.branch)

    def test_queryset_non_manager(self):
        request = self.request_factory.get(reverse('admin:branches_branch_changelist'))
        request.user = self.normal_staff_user
        self.assertEqual(self.model_admin.get_queryset(request).count(), 0)

    def test_super_user(self):
        request = self.request_factory.get(reverse('admin:branches_branch_changelist'))
        request.user = self.super_user

        self.assertTrue(self.model_admin.has_module_permission(request))
        self.assertTrue(self.model_admin.has_view_permission(request, self.branch))
        self.assertTrue(self.model_admin.has_view_permission(request))
        self.assertEqual(self.model_admin.get_queryset(request).count(), 2)

    def test_formfield_for_foreignkey(self):
        request = self.request_factory.get(reverse('admin:branches_branch_add'))
        result = self.model_admin.formfield_for_foreignkey(Branch.manager.field, request)
        self.assertEqual(result.queryset.count(), 1)
