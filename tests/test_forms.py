import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

os.environ["DJANGO_SETTINGS_MODULE"] = "server.app.settings"

import django
django.setup()

from django.test import TestCase
from backend.server.server.forms import UserAccountForm, UserPickedOptionSerializer

class TestUserAccountForm(TestCase):
    def test_valid_data(self):
        form = UserAccountForm(data={"email": "test@example.com", "password": "securepass"})
        self.assertTrue(form.is_valid())

    def test_missing_email(self):
        form = UserAccountForm(data={"email": "", "password": "securepass"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_password(self):
        form = UserAccountForm(data={"email": "test@example.com", "password": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)


class TestUserPickedOptionSerializer(TestCase):
    def test_valid_data(self):
        form = UserPickedOptionSerializer(
            data={"selectedOption": "Option A", "date": "2024-01-30", "selectedOdds": 2.5, "stake": 100}
        )
        self.assertTrue(form.is_valid())

    def test_missing_selected_option(self):
        form = UserPickedOptionSerializer(
            data={"selectedOption": "", "date": "2024-01-30", "selectedOdds": 2.5, "stake": 100}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("selectedOption", form.errors)

    # def test_negative_stake(self):
    #     form = UserPickedOptionSerializer(
    #         data={"selectedOption": "Option A", "date": "2024-01-30", "selectedOdds": 2.5, "stake": -10}
    #     )
    #     self.assertFalse(form.is_valid())
    #     self.assertIn("stake", form.errors)
