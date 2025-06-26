from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from .models import Client


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
