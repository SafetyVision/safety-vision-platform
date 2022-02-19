from rest_framework import serializers
from .models import Device
from locations.models import Location
import boto3
from botocore.config import Config


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'serial_number', 'location', 'description']
        read_only_fields = ['id', 'serial_number']

    def update(self, instance, validated_data):
        region = 'us-east-1'
        stream_name=f'SafetyVision-VS-{instance.serial_number}'

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

        instance.description = validated_data['description']
        instance.location = validated_data['location']
        instance.stream_arn = streamArn
        instance.save()

        return instance
