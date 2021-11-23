from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import serializers
from .models import Account

class ListCreateAccountAPIView(ListCreateAPIView):
    serializer_class = serializers.CreateAccountSerializer
    permissions_classes = [AllowAny]

    def get_queryset(self):
        return Account.objects.filter(id=self.request.user.account.id)


class GetUpdateDeleteAccountAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.GetUpdateDeleteAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(id=self.request.user.account.id)
