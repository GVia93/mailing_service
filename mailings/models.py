from django.conf import settings
from django.db import models


class Client(models.Model):
    """Получатель рассылки: email, ФИО и комментарий."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Владелец",
    )
    email = models.EmailField(unique=True, verbose_name="mail")
    full_name = models.CharField(max_length=100, verbose_name="Клиент")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        permissions = [
            ("can_view_all_clients", "Может просматривать всех клиентов"),
        ]

    def __str__(self):
        return self.full_name


class Message(models.Model):
    """Сообщение для рассылки: тема и тело письма."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Владелец",
    )
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(blank=True, verbose_name="Тело письма")

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    """Рассылка сообщений: время старта/окончания, статус, связанное сообщение и клиенты."""

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Начало рассылки")
    end_time = models.DateTimeField(verbose_name="Конец рассылки")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="created", verbose_name="Статус"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_view_all_mailings", "Может просматривать все рассылки"),
            ("can_toggle_mailing", "Может отключать/включать рассылки"),
        ]

    def __str__(self):
        return f"{self.message.subject} ({self.get_status_display()})"


class Attempt(models.Model):
    """Попытка отправки письма: статус, время, ответ почтового сервера и связь с рассылкой."""

    STATUS_CHOICES = [("success", "Успешно"), ("failed", "Не успешно")]

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="attempts"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.mailing} — {self.get_status_display()} — {self.created_at:%Y-%m-%d %H:%M}"
