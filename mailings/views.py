from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView

from .forms import MailingForm
from .models import Client, Message, Mailing, Attempt


class ClientListView(ListView):
    model = Client
    template_name = 'mailings/client_list.html'


class ClientCreateView(CreateView):
    model =Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/client_from.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/client_from.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailings/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')


class AttemptListView(ListView):
    model = Attempt
    template_name = 'mailings/attempt_list.html'
