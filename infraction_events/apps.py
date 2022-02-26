from django.apps import AppConfig
from django.db.models.signals import pre_delete
from .receivers import delete_infraction_event_video_clip


class InfractionEventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infraction_events'

    def ready(self):
        pre_delete.connect(delete_infraction_event_video_clip, sender='infraction_events.InfractionEvent')
