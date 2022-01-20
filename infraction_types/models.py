from django.db import models

class InfractionType(models.Model):
    infraction_type_name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # Parameters to add later
    # created_by = models.CharField(max_length=75)



