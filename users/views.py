from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import ExtendedUser

class ListCreateUsersAPIView(ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account = self.request.user.account
        return ExtendedUser.objects.filter(account=account)

class RetrieveUpdateDestroyUsersAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account = self.request.user.account
        return ExtendedUser.objects.filter(account=account)
