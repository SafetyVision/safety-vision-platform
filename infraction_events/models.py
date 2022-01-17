from django.db import models
from video_clips.models import VideoClip
from accounts.models import Account

class InfractionEvent(models.Model):
  account = models.ForeignKey(
    Account,
    on_delete=models.CASCADE,
  )
  infraction_date_time = models.DateTimeField()
  infraction_video = models.OneToOneField(
    VideoClip,
    on_delete=models.SET_NULL,
    null=True
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
