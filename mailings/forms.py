from django import forms

from .models import Client, Mailing, Message


class MailingForm(forms.ModelForm):
    """
    Форма создания/редактирования рассылки с выбором даты и времени.
    Ограничивает выбор сообщений и клиентов только текущим пользователем.
    """

    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "clients"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["clients"].queryset = Client.objects.filter(owner=user)
        self.fields["message"].queryset = Message.objects.filter(owner=user)


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ["email", "full_name", "comment"]


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ["subject", "body"]
