from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import serializers
from . import models

class CreateAccountAPIView(CreateAPIView):
    serializer_class = serializers.CreateAccountSerializer
    permissions_classes = [AllowAny]


class GetUpdateDeleteAccountAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.GetUpdateDeleteAccountSerializer
    queryset = models.Account.objects.all()
    permission_classes = [IsAuthenticated]
