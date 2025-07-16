from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, ProfileUpdateForm
from .models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля текущего пользователя.
    Доступно только авторизованным пользователям.
    Использует форму ProfileUpdateForm и обновляет модель CustomUser.
    После сохранения перенаправляет на главную страницу.
    """

    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """
        Возвращает объект текущего пользователя.
        """
        return self.request.user


class RegisterView(CreateView):
    """Регистрация нового пользователя."""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class CustomLoginView(LoginView):
    """Вход пользователя в систему."""
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    """Выход пользователя из системы."""
    next_page = reverse_lazy('users:login')


class CustomPasswordResetView(PasswordResetView):
    """Запрос сброса пароля."""
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Подтверждение сброса пароля по ссылке из письма."""
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')
