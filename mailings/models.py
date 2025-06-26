from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='mail')
    full_name = models.CharField(max_length=100, verbose_name='Клиент')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(blank=True, verbose_name='Тело письма')

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Начало рассылки')
    end_time = models.DateTimeField(verbose_name='Конец рассылки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')

    def __str__(self):
        return f'{self.message.subject} ({self.get_status_display()})'


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно')
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')

    def __str__(self):
        return f"{self.mailing} — {self.get_status_display()} — {self.created_at:%Y-%m-%d %H:%M}"
