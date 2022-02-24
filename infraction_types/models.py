from django.db import models
from devices.models import Device
from accounts.models import Account

class InfractionType(models.Model):
    infraction_type_name = models.CharField(max_length=100)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='infraction_types'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
