from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from .forms import ClientForm, MailingForm, MessageForm
from .models import Attempt, Client, Mailing, Message
from .utils import send_mailing


class MailingToggleStatusView(LoginRequiredMixin, View):
    """Включает или отключает рассылку."""

    def post(self, request, pk, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=pk)

        if request.user != mailing.owner and not request.user.is_manager:
            raise PermissionDenied("Нет прав для изменения статуса рассылки.")

        if mailing.status == "started":
            mailing.status = "completed"
            mailing.save(update_fields=["status"])
        elif mailing.status == "created" or "completed":
            mailing.status = "started"
            mailing.save(update_fields=["status"])
            send_mailing(mailing)

        return redirect("mailings:mailing_list")


@method_decorator(cache_control(private=True, max_age=600), name="dispatch")
class AttemptListView(LoginRequiredMixin, ListView):
    """Показывает список попыток рассылки."""

    model = Attempt
    template_name = "mailings/attempt_list.html"

    def get_queryset(self):
        return Attempt.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        mailings = Mailing.objects.filter(owner=user)
        attempts = Attempt.objects.filter(mailing__in=mailings)

        context["total_attempts"] = attempts.count()
        context["success_attempts"] = attempts.filter(status="success").count()
        context["failed_attempts"] = attempts.filter(status="failed").count()
        context["messages_sent"] = attempts.filter(status="success").count()

        return context


@method_decorator(cache_control(private=True, max_age=600), name="dispatch")
class ClientListView(LoginRequiredMixin, ListView):
    """Выводит список всех клиентов."""

    model = Client
    template_name = "mailings/client_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создает нового клиента."""

    model = Client
    form_class = ClientForm
    template_name = "mailings/client_from.html"
    success_url = reverse_lazy("mailings:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует данные клиента."""

    model = Client
    form_class = ClientForm
    template_name = "mailings/client_from.html"
    success_url = reverse_lazy("mailings:client_list")

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет клиента."""

    model = Client
    template_name = "mailings/client_confirm_delete.html"
    success_url = reverse_lazy("mailings:client_list")

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


@method_decorator(cache_control(private=True, max_age=600), name="dispatch")
class MessageListView(LoginRequiredMixin, ListView):
    """Выводит список всех сообщений."""

    model = Message
    template_name = "mailings/message_list.html"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создает новое сообщение."""

    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует сообщение."""

    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет сообщение."""

    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


@method_decorator(cache_control(private=True, max_age=600), name="dispatch")
class MailingListView(LoginRequiredMixin, ListView):
    """Выводит список всех рассылок."""

    model = Mailing
    template_name = "mailings/mailing_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создает новую рассылку."""

    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        """
        Установка текущего пользователя как владельца.
        """
        form.instance.owner = self.request.user
        form.instance.status = "created"
        return super().form_valid(form)

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        """
        Добавляет текущего пользователя в параметры формы.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует рассылку."""

    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        form.instance.status = "created"
        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Добавляет текущего пользователя в параметры формы.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет рассылку."""

    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


@method_decorator(cache_control(public=True, max_age=600), name="dispatch")
class HomeView(TemplateView):
    """
    Главная страница со статистикой. Серверное кеширование на 10 минут.
    """

    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats = cache.get("home_stats")
        if not stats:
            stats = {
                "total_mailings": Mailing.objects.count(),
                "active_mailings": Mailing.objects.filter(status="started").count(),
                "unique_clients": Client.objects.values("email").distinct().count(),
            }
            cache.set("home_stats", stats, 60 * 10)

        context.update(stats)
        return context
