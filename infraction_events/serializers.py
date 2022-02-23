import boto3
from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from .models import InfractionEvent
from video_clips.serializers import VideoClipSerializer
from video_clips.models import VideoClip
from django.core.files.base import ContentFile
from django_eventstream import send_event

class InfractionEventSerializer(ModelSerializer):
  infraction_video = VideoClipSerializer(read_only=True)

  class Meta:
    model = InfractionEvent
    fields = ['id', 'infraction_type', 'infraction_video', 'infraction_date_time']

class InfractionEventCreateSerializer(ModelSerializer):
  class Meta:
    model = InfractionEvent
    fields = ['infraction_type', 'infraction_date_time']

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

    infraction_event = InfractionEvent.objects.create(
      infraction_type=validated_data['infraction_type'],
      infraction_date_time=validated_data['infraction_date_time'],
      infraction_video=infraction_video,
    )

    send_event(
      f'account_{infraction_event.infraction_type.device.location.account.id}_events',
      'message',
      {'text': f'New infraction event #{infraction_event.id} detected'}
    )

    return infraction_event
