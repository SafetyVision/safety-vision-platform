from rest_framework import serializers
from .models import Device

class CreateDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['location', 'stream_name']

class DeviceSerializer(serializers.ModelSerializer):
    stream_url = serializers.CharField(source='getStreamUrl', max_length=1000)

    class Meta:
        model = Device
        fields = ['id', 'location', 'stream_name','stream_url']
