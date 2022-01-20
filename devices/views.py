from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Device

class CreateDeviceAPIView(CreateAPIView):
    serializer_class = serializers.CreateDeviceSerializer
    permission_classes = [IsAuthenticated]

class ListDeviceAPIView(ListAPIView):
    serializer_class = serializers.DeviceSerializer
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()
    # def get_queryset(self):
    #     return Device.objects.filter(id=self.request.user.device.id)

class GetUpdateDeleteDeviceAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.DeviceSerializer
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()

    # def get_queryset(self):
    #     return Device.objects.filter(id=self.request.user.Device.id)