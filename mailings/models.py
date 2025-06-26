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
