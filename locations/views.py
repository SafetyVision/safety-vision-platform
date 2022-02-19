from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Location
from devices.models import Device
from infraction_types.models import InfractionType
import boto3
from botocore.config import Config

class ListCreateLocationAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Location.objects.filter(account=self.request.user.account)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateUpdateLocationSerializer
        return serializers.ListGetLocationSerializer

class RetrieveUpdateDeleteLocationAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Location.objects.filter(account=self.request.user.account)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ListGetLocationSerializer
        return serializers.CreateUpdateLocationSerializer

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
                pass
            finally:
                device.description = ''
                device.save()

                infraction_types = InfractionType.objects.filter(device=device)
                for infraction_type in infraction_types:
                    infraction_type.delete()

        instance.delete()
