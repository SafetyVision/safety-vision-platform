from django.db import models
from devices.models import Device
from infraction_types.models import InfractionType

class PredictionModel(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    infraction_type = models.ForeignKey(InfractionType, on_delete=models.CASCADE)
    is_predicting = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Detecting {self.infraction_type.infraction_type_name} on device #{self.device.serial_number}'
