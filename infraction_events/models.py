from django.db import models
from video_clips.models import VideoClip
from infraction_types.models import InfractionType

class InfractionEvent(models.Model):
  infraction_type = models.ForeignKey(
    InfractionType,
    on_delete=models.CASCADE,
    null=True,
  )
  infraction_date_time = models.DateTimeField()
  infraction_video = models.OneToOneField(
    VideoClip,
    on_delete=models.SET_NULL,
    null=True
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
