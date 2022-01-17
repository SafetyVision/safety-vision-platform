import string
import random
from rest_framework.serializers import ModelSerializer
from .models import InfractionEvent
from video_clips.serializers import VideoClipSerializer
from video_clips.models import VideoClip
from django.core.files.base import File

class InfractionEventSerializer(ModelSerializer):
  infraction_video = VideoClipSerializer(read_only=True)

  class Meta:
    model = InfractionEvent
    fields = ['id', 'account', 'infraction_video', 'infraction_date_time']

class InfractionEventCreateSerializer(ModelSerializer):
  class Meta:
    model = InfractionEvent
    fields = ['account', 'infraction_date_time']

  def create(self, validated_data):
    infraction_video = VideoClip()
    # TODO download the file from Kinesis
    file = open('/code/media/test.mp4', 'rb')
    infraction_video.file.save('blah.mp4', File(file))
    infraction_video.save()

    return InfractionEvent.objects.create(
      account=validated_data['account'],
      infraction_date_time=validated_data['infraction_date_time'],
      infraction_video=infraction_video,
    )
