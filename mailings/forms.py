from django import forms
from .models import Mailing

class MailingForm(forms.ModelForm):
    """Форма создания/редактирования рассылки с выбором даты и времени через input type="datetime-local"."""

    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'status', 'message', 'clients']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
