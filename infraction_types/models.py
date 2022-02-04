from django.db import models
from devices.models import Device

class InfractionType(models.Model):
    infraction_type_name = models.CharField(max_length=100)
    device = models.ForeignKey(
        Device,
        related_name='devices',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
