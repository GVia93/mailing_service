from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone', 'country', 'password1', 'password2')


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма редактирования профиля.
    """

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "country",
            "avatar",
        ]
