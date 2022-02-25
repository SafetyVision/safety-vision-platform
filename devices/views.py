from curses.ascii import HT
from django.http import Http404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from . import serializers
from prediction_models.serializers import PredictionModelSerializer
from .models import Device
from prediction_models.models import PredictionModel
from infraction_types.models import InfractionType
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
            instance.infraction_type_models.clear()
            instance.description = ''
            instance.location = None
            instance.stream_arn = ''
            instance.save()

class ListCreatePredictionModelAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PredictionModelSerializer

    def get_queryset(self):
        try:
            account = self.request.user.account
            devices = Device.objects.filter(location__account=account)
            device = devices.get(serial_number=self.kwargs['serial_number'])

            return PredictionModel.objects.filter(device=device)
        except:
            raise Http404('Device not found')

class RetrieveDeletePredictionModelAPIView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PredictionModelSerializer

    def get_queryset(self):
        return PredictionModel.objects.filter(device__location__account=self.request.user.account)

    def get_object(self):
        try:
            account = self.request.user.account

            devices = Device.objects.filter(location__account=account)
            device = devices.get(serial_number=self.kwargs['serial_number'])

            infraction_types = InfractionType.objects.filter(account=account)
            infraction_type = infraction_types.get(id=self.kwargs['infraction_type'])

            return PredictionModel.objects.get(device=device, infraction_type=infraction_type)
        except:
            raise Http404('Could not get prediction model')
