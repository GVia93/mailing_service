from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from .forms import MailingForm
from .models import Attempt, Client, Mailing, Message
from .utils import send_mailing


class StatsView(LoginRequiredMixin, TemplateView):
    """
    Отображает статистику по попыткам рассылок текущего пользователя.
    """

    template_name = "mailings/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = Mailing.objects.filter(owner=self.request.user)

        context["total_attempts"] = Attempt.objects.filter(mailing__in=mailings).count()
        context["success_attempts"] = Attempt.objects.filter(
            mailing__in=mailings, status="success"
        ).count()
        context["failed_attempts"] = Attempt.objects.filter(
            mailing__in=mailings, status="failed"
        ).count()
        context["messages_sent"] = Attempt.objects.filter(
            mailing__in=mailings, status="success"
        ).count()

        return context


class ClientListView(ListView):
    """Выводит список всех клиентов."""

    model = Client
    template_name = "mailings/client_list.html"


class ClientCreateView(CreateView):
    """Создает нового клиента."""

    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailings/client_from.html"
    success_url = reverse_lazy("mailings:client_list")


class ClientUpdateView(UpdateView):
    """Редактирует данные клиента."""

    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailings/client_from.html"
    success_url = reverse_lazy("mailings:client_list")


class ClientDeleteView(DeleteView):
    """Удаляет клиента."""

    model = Client
    template_name = "mailings/client_confirm_delete.html"
    success_url = reverse_lazy("mailings:client_list")


class MessageListView(ListView):
    """Выводит список всех сообщений."""

    model = Message
    template_name = "mailings/message_list.html"


class MessageCreateView(CreateView):
    """Создает новое сообщение."""

    model = Message
    fields = ["subject", "body"]
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")


class MessageUpdateView(UpdateView):
    """Редактирует сообщение."""

    model = Message
    fields = ["subject", "body"]
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")


class MessageDeleteView(DeleteView):
    """Удаляет сообщение."""

    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")


class MailingListView(ListView):
    """Выводит список всех рассылок."""

    model = Mailing
    template_name = "mailings/mailing_list.html"


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
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    """Редактирует рассылку."""

    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")


class MailingDeleteView(DeleteView):
    """Удаляет рассылку."""

    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")


class HomeView(TemplateView):
    """ """

    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status="started").count()
        context["unique_clients"] = Client.objects.values("email").distinct().count()
        return context


def run_mailing(request, pk):
    """Ручной запуск рассылки и фиксация попыток отправки."""

    mailing = get_object_or_404(Mailing, pk=pk)
    send_mailing(mailing)
    messages.success(request, "Рассылка запущена.")
    return redirect("mailings:mailing_list")
