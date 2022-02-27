from django.db import models
from devices.models import Device
from infraction_types.models import InfractionType

class PredictionModel(models.Model):
    class TrainingState(models.TextChoices):
        INITIALIZED = 'init', 'Initialized'
        FIRST_COMMITTING_INFRACTION = 'committing_1', 'First committing infraction'
        FIRST_DONE_COMMITTING_INFRACTION = 'done_committing_1', 'Done committing first infraction'
        FIRST_NOT_COMMITTING_INFRACTION = 'not_committing_1', 'First not committing infraction'
        FIRST_DONE_NOT_COMMITTING_INFRACTION = 'done_not_committing_1', 'First done not commimtting infraction'
        SECOND_COMMITTING_INFRACTION = 'committing_2', 'Second committing infraction'
        SECOND_DONE_COMMITTING_INFRACTION = 'done_committing_2', 'Done committing second infraction'
        SECOND_NOT_COMMITTING_INFRACTION = 'not_committing_2', 'Second not committing infraction'
        SECOND_DONE_NOT_COMMITTING_INFRACTION = 'done_not_committing_2', 'Done not commimtting second infraction'
        TRAINED = 'trained', 'Trained'

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    infraction_type = models.ForeignKey(InfractionType, on_delete=models.CASCADE)
    is_predicting = models.BooleanField(default=False)
    training_state = models.CharField(
        max_length=21,
        choices=TrainingState.choices,
        default=TrainingState.INITIALIZED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Detecting {self.infraction_type.infraction_type_name} on device #{self.device.serial_number}'
