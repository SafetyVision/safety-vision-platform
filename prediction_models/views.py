from django.http import Http404
from rest_framework.generics import RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import PredictionModel
from devices.models import Device
from infraction_types.models import InfractionType

class CreatePredictionModelAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PredictionModelSerializer

    def get_queryset(self):
        return PredictionModel.objects.filter(device__location__account=self.request.user.account)

class RetrieveDeletePredictionModelAPIView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PredictionModelSerializer

    def get_queryset(self):
        return PredictionModel.objects.filter(device__location__account=self.request.user.account)

    def get_object(self):
        try:
            account = self.request.user.account

            devices = Device.objects.filter(location__account=account)
            device = devices.get(serial_number=self.kwargs['device'])

            infraction_types = InfractionType.objects.filter(account=account)
            infraction_type = infraction_types.get(id=self.kwargs['infraction_type'])

            return PredictionModel.objects.get(device=device, infraction_type=infraction_type)
        except:
            raise Http404('Could not get prediction model')

