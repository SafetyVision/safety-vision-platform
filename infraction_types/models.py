from django.db import models
from accounts.models import Account

class InfractionType(models.Model):
    infraction_type_name = models.CharField(max_length=100)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='infraction_types',
        null=True,
        default=None,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.infraction_type_name
