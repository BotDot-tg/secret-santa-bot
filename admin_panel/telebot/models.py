from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Clients(models.Model):
    telegram_id = models.BigIntegerField(
        verbose_name='Telegram ID'
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=500,
        null=True
    )