import boto3
from datetime import timedelta
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import InfractionEvent
from video_clips.serializers import VideoClipSerializer
from video_clips.models import VideoClip
from prediction_models.models import PredictionModel
from django.core.files.base import ContentFile
from django_eventstream import send_event
from devices.serializers import DeviceRelatedField
from locations.serializers import LocationRelatedField
from infraction_types.serializers import InfractionTypeRelatedField

class InfractionEventSerializer(ModelSerializer):
  infraction_video = VideoClipSerializer(read_only=True)
  location = LocationRelatedField()
  infraction_type = InfractionTypeRelatedField()

  class Meta:
    model = InfractionEvent
    fields = ['id', 'infraction_type', 'infraction_video', 'location', 'infraction_date_time']

class InfractionEventCreateSerializer(ModelSerializer):
  device = DeviceRelatedField(write_only=True)

  class Meta:
    model = InfractionEvent
    fields = ['infraction_date_time', 'infraction_type', 'device', 'location']
    read_only_fields = ['location']

  def validate(self, data):
    try:
      PredictionModel.objects.get(
        device=data['device'],
        infraction_type=data['infraction_type']
      )
      return super(InfractionEventCreateSerializer, self).validate(data)
    except:
      raise ValidationError()


  def create(self, validated_data):
    model = PredictionModel.objects.get(
      device=validated_data['device'],
      infraction_type=validated_data['infraction_type']
    )
    stream_name = f'SafetyVision-VS-{model.device.serial_number}'

    try:
      client = boto3.client(
        'kinesisvideo',
        region_name='us-east-1',
      )
      endpoint_response = client.get_data_endpoint(
        StreamName=stream_name,
        APIName='GET_CLIP'
      )
      endpoint_url = endpoint_response['DataEndpoint']

      client = boto3.client(
        'kinesis-video-archived-media',
        endpoint_url=endpoint_url,
        region_name='us-east-1',
      )
      clip_response = client.get_clip(
        StreamName=stream_name,
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
      file_name = f'{infraction_video.id}_{validated_data["infraction_date_time"]}.mp4'
      infraction_video.file.save(file_name, clip_file)
    except:
      infraction_video = None

    infraction_event = InfractionEvent.objects.create(
      infraction_type=model.infraction_type,
      infraction_date_time=validated_data['infraction_date_time'],
      location=model.device.location,
      infraction_video=infraction_video,
    )

    send_event(
      f'account_{infraction_event.location.account.id}_events',
      'message',
      {'infraction_event': infraction_event.id}
    )

    return infraction_event
