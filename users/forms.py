from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone', 'country', 'password1', 'password2')
