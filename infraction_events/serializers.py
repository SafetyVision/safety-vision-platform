import boto3
from botocore.config import Config
from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from .models import InfractionEvent
from video_clips.serializers import VideoClipSerializer
from video_clips.models import VideoClip
from django.core.files.base import ContentFile

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
    client = boto3.client(
      'kinesisvideo',
      config=Config(region_name='us-east-1'),
    )
    endpoint_response = client.get_data_endpoint(
      StreamARN='arn:aws:kinesisvideo:us-east-1:368242569276:stream/SafetyVision-VS-1/1642016630351',
      APIName='GET_CLIP'
    )
    endpoint_url = endpoint_response['DataEndpoint']

    client = boto3.client(
      'kinesis-video-archived-media',
      endpoint_url=endpoint_url,
      config=Config(region_name='us-east-1')
    )
    clip_response = client.get_clip(
      StreamARN='arn:aws:kinesisvideo:us-east-1:368242569276:stream/SafetyVision-VS-1/1642016630351',
      ClipFragmentSelector={
        'FragmentSelectorType': 'SERVER_TIMESTAMP',
        'TimestampRange': {
          'StartTimestamp': validated_data['infraction_date_time'] - timedelta(seconds=5),
          'EndTimestamp': validated_data['infraction_date_time'] + timedelta(seconds=5),
        }
      }
    )

    clip_file = ContentFile(b'')
    for chunk in clip_response['Payload'].iter_chunks():
      clip_file.write(chunk)

    infraction_video = VideoClip()
    infraction_video.save()
    file_name = str(infraction_video.id) + '_' + str(validated_data['infraction_date_time']) + '.mp4'
    infraction_video.file.save(file_name, clip_file)

    return InfractionEvent.objects.create(
      account=validated_data['account'],
      infraction_date_time=validated_data['infraction_date_time'],
      infraction_video=infraction_video,
    )
