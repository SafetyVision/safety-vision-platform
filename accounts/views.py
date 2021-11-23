from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Account

class CreateAccountAPIView(CreateAPIView):
    serializer_class = serializers.CreateAccountSerializer
    authentication_classes = []

class ListAccountAPIView(ListAPIView):
    serializer_class = serializers.CreateAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(id=self.request.user.account.id)

class GetUpdateDeleteAccountAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.GetUpdateDeleteAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(id=self.request.user.account.id)
