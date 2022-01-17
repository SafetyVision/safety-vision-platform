from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import InfractionEvent
from .permissions import IsPredictionServiceRequest

class ListCreateInfractionEventsAPIView(ListAPIView):
  serializer_class = serializers.InfractionEventSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    account = self.request.user.account
    return InfractionEvent.objects.filter(account=account)

class GetDeleteInfractionEventsAPIView(RetrieveDestroyAPIView):
  serializer_class = serializers.InfractionEventSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    account = self.request.user.account
    return InfractionEvent.objects.filter(account=account)

class PostInfractionEventsAPIView(CreateAPIView):
  serializer_class = serializers.InfractionEventCreateSerializer
  permission_classes = [IsPredictionServiceRequest]
  authentication_classes = []
