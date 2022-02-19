from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from . import serializers
from .models import Device
import boto3
from botocore.config import Config

class RetrieveUpdateDeleteDeviceAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'serial_number'
    serializer_class = serializers.DeviceSerializer
    queryset = Device.objects.all()

    def perform_destroy(self, instance):
        try:
            region = 'us-east-1'
            client = boto3.client(
                'kinesisvideo',
                config=Config(region_name=region),
            )

            client.delete_stream(
                StreamARN=instance.stream_arn
            )
        except:
            raise ValidationError("Failed to delete device stream")
        else:
            instance.description = ''
            instance.location = None
            instance.stream_arn = ''
            instance.save()
