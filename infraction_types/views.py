from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import InfractionType

class CreateInfractionTypeAPIView(CreateAPIView):
    serializer_class = serializers.CreateInfractionTypeSerializer
    permission_classes = [IsAuthenticated]

class ListInfractionTypesAPIView(ListAPIView):
    serializer_class = serializers.ListInfractionTypesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InfractionType.objects
