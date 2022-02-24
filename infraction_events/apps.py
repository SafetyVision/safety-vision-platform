from django.apps import AppConfig
from django.db.models.signals import pre_delete
from .receivers import deleteInfractionEventVideoClip


class InfractionEventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infraction_events'

    def ready(self):
        pre_delete.connect(deleteInfractionEventVideoClip, sender='infraction_events.InfractionEvent')
