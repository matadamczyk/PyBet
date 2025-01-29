from django import forms
from .models import UserAccount, UserPickedOption

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['email', 'password']


class UserPickedOptionSerializer(forms.ModelForm):
    class Meta:
        model = UserPickedOption
        fields = ['selectedOption', 'date', 'selectedOdds', 'stake']

