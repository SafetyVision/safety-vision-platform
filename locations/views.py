from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from . import serializers
from .models import Location
from devices.models import Device
from infraction_types.models import InfractionType
import boto3
from botocore.config import Config

class ListCreateLocationAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LocationSerializer

    def get_queryset(self):
        return Location.objects.filter(account=self.request.user.account)

class RetrieveUpdateDeleteLocationAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LocationSerializer

    def get_queryset(self):
        return Location.objects.filter(account=self.request.user.account)

    def perform_destroy(self, instance):
        devices = Device.objects.filter(location=instance)
        region = 'us-east-1'
        for device in devices:
            try:
                client = boto3.client(
                    'kinesisvideo',
                    config=Config(region_name=region),
                )

                client.delete_stream(
                    StreamARN=device.stream_arn
                )
            except:
                raise ValidationError(f'Failed to delete stream for device {device.serial_number}')
            else:
                device.infraction_type_models.clear()
                device.description = ''
                device.stream_arn = ''
                device.save()

        instance.delete()
