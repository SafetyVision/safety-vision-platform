from django.db import models
from accounts.models import Account

class Location(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
