from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from .forms import ProfileUpdateForm, UserRegisterForm
from .tokens import account_activation_token

User = get_user_model()


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Представление для отображения списка пользователей.
    Доступно только менеджерам.
    """

    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

    def test_func(self):
        return self.request.user.is_manager


class UserBlockToggleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Представление для блокировки или разблокировки пользователя.
    Меняет статус is_active у пользователя. Доступно только менеджерам.
    """

    model = User
    fields = []

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if user.is_superuser:
            raise PermissionDenied("Нельзя блокировать суперпользователя.")

        user.is_active = not user.is_active
        user.save()
        status = "разблокирован" if user.is_active else "заблокирован"
        messages.success(request, f"Пользователь {user.email} {status}.")
        return redirect("users:user_list")

    def test_func(self):
        return self.request.user.is_manager


class ActivateView(View):
    """
    Представление для активации пользователя по email-ссылке.
    Проверяет валидность токена, активирует аккаунт и перенаправляет на страницу входа.
    """

    def get(self, request, uidb64, token):
        """
        Обрабатывает GET-запрос по ссылке подтверждения регистрации.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("users:login")
        return redirect("users:register")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля текущего пользователя.
    Доступно только авторизованным пользователям.
    Использует форму ProfileUpdateForm.
    """

    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """
        Возвращает текущего авторизованного пользователя.
        """
        return self.request.user


class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.
    После регистрации отправляется email для подтверждения.
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """
        Обработка валидной формы регистрации.
        Создаёт неактивного пользователя и отправляет письмо с ссылкой активации.
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = self.request.build_absolute_uri(
            reverse("users:activate", kwargs={"uidb64": uid, "token": token})
        )

        send_mail(
            "Подтверждение регистрации",
            f"Перейдите по ссылке для активации: {activation_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return redirect("users:login")


class CustomLoginView(LoginView):
    """
    Представление для входа пользователя в систему.
    Использует стандартную форму и шаблон users/login.html.
    """

    template_name = "users/login.html"


class CustomLogoutView(LogoutView):
    """
    Представление для выхода пользователя из системы.
    После выхода перенаправляет на страницу входа.
    """

    next_page = reverse_lazy("users:login")


class CustomPasswordResetView(PasswordResetView):
    """
    Представление для запроса сброса пароля.
    Отправляет письмо со ссылкой на смену пароля.
    """

    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Представление для подтверждения сброса пароля.
    Отображает форму ввода нового пароля.
    """

    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:login")
