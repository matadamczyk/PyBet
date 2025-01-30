from django import forms
from .models import UserAccount, UserPickedOption


class UserAccountForm(forms.ModelForm):
    class Meta:
        app_label = "server"
        model = UserAccount
        fields = ["email", "password"]


class UserPickedOptionSerializer(forms.ModelForm):
    class Meta:
        app_label = "server"
        model = UserPickedOption
        fields = ["selectedOption", "date", "selectedOdds", "stake"]
