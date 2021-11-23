from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.models import Account

class ExtendedUser(AbstractUser):
    account = models.ForeignKey(
        Account,
        related_name='users',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True)
