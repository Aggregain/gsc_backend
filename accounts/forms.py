from unfold.forms import UserChangeForm, UserCreationForm

from .models import Account


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('first_name', 'second_name', 'last_name', 'email', 'avatar')


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('first_name', 'second_name', 'last_name', 'email', 'avatar')
