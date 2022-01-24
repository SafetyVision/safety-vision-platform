from asyncio import sleep
from socket import timeout
from rest_framework import serializers
from .models import Device
import boto3
from botocore.config import Config

class CreateDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['serial_number', 'location']

    def create(self, validated_data):
        region = 'us-east-1'
        stream_name='SafetyVision-VS-'+validated_data['serial_number']
        
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
            
        device = Device(
            **validated_data,
            stream_arn=streamArn
        )
        device.save()

        return device

class DeviceSerializer(serializers.ModelSerializer):
    stream_url = serializers.CharField(source='getStreamUrl', max_length=1000)

    class Meta:
        model = Device
        fields = ['id', 'serial_number', 'location','stream_url']
