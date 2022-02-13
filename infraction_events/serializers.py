import boto3
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
    fields = ['id', 'account', 'infraction_video', 'infraction_date_time', 'location']

class InfractionEventCreateSerializer(ModelSerializer):
  class Meta:
    model = InfractionEvent
    fields = ['account', 'infraction_date_time', 'location']

  def create(self, validated_data):
    client = boto3.client(
      'kinesisvideo',
      region_name='us-east-1',
    )
    endpoint_response = client.get_data_endpoint(
      StreamName='SafetyVision-VS-2',
      APIName='GET_CLIP'
    )
    endpoint_url = endpoint_response['DataEndpoint']

    client = boto3.client(
      'kinesis-video-archived-media',
      endpoint_url=endpoint_url,
      region_name='us-east-1',
    )
    clip_response = client.get_clip(
      StreamName='SafetyVision-VS-2',
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
      location=validated_data['location'],
      infraction_date_time=validated_data['infraction_date_time'],
      infraction_video=infraction_video,
    )
