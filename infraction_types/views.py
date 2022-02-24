from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import InfractionType

class ListCreateInfractionTypesAPIView(ListCreateAPIView):
    serializer_class = serializers.InfractionTypesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account = self.request.user.account
        return InfractionType.objects.filter(account=account)

class RetrieveUpdateDestroyInfractionTypesAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.InfractionTypesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account = self.request.user.account
        return InfractionType.objects.filter(account=account)
