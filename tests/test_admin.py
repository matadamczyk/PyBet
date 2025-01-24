import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.server.app.settings'

import django
django.setup()

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from backend.server.server.admin import UserAccountAdmin
from backend.server.server.models import UserAccount


class MockRequest:
    pass

class TestUserAccountAdmin(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.admin = UserAccountAdmin(UserAccount, self.site)
        self.user = get_user_model().objects.create_user(
            email="1@gmail.com",
            password="pass",
            is_staff=True,
            is_active=True,
        )
        self.request = MockRequest()

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ('email', 'is_staff', 'is_active'))

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ('email', 'is_staff', 'is_active'))

    def test_fieldsets(self):
        self.assertEqual(
            self.admin.fieldsets,
            (
                (None, {'fields': ('email', 'password')}),
                ('Permissions', {'fields': ('is_staff', 'is_active')}),
            ),
        )

    def test_add_fieldsets(self):
        self.assertEqual(
            self.admin.add_fieldsets,
            (
                (None, {
                    'classes': ('wide',),
                    'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
                ),
            ),
        )

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ('email',))

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ('email',))

    def test_queryset(self):
        queryset = self.admin.get_queryset(self.request)
        self.assertIn(self.user, queryset)
