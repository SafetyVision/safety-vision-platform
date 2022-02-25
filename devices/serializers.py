from rest_framework import serializers
from .models import Device
import boto3
from botocore.config import Config

class DeviceRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance.description

    def to_representation(self, instance):
        return instance.serial_number

    def to_internal_value(self, data):
        return Device.objects.get(serial_number=data)

    def get_queryset(self):
        return Device.objects.all()


class DeviceSerializer(serializers.ModelSerializer):
    stream_url = serializers.CharField(
        source='getStreamUrl',
        max_length=1000,
        read_only=True
    )

    class Meta:
        model = Device
        fields = ['serial_number', 'location', 'description', 'stream_url']
        read_only_fields = ['serial_number', 'stream_url']
        lookup_field = 'serial_number'

    def update(self, instance, validated_data):
        region = 'us-east-1'
        stream_name=f'SafetyVision-VS-{instance.serial_number}'

        if not instance.stream_arn:
            client = boto3.client(
                'kinesisvideo',
                config=Config(region_name=region),
            )

            try:
                stream = client.describe_stream(
                    StreamName=stream_name
                )
                streamArn = stream['StreamInfo']['StreamARN']
            except:
                stream = client.create_stream(
                    StreamName=stream_name,
                    DataRetentionInHours=1
                )
                streamArn = stream['StreamARN']
            finally:
                instance.stream_arn = streamArn


        instance.description = validated_data['description']
        instance.location = validated_data['location']
        instance.save()

        return instance
