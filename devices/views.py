from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Device
import boto3
from botocore.config import Config

class CreateDeviceAPIView(CreateAPIView):
    serializer_class = serializers.CreateDeviceSerializer
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()

class ListDeviceAPIView(ListAPIView):
    serializer_class = serializers.DeviceSerializer
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()

class GetUpdateDeleteDeviceAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.DeviceSerializer
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()

    def perform_destroy(self, instance):
        region = 'us-east-1'

        try:
            client = boto3.client(
                'kinesisvideo',
                config=Config(region_name=region),
            )

            client.delete_stream(
                StreamARN=instance.stream_arn
            )
        except:
            raise serializers.ValidationError("Failed to delete device stream")

        instance.delete()
