from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import ExtendedUser
from .permissions import UserPermissions, IsAccountOwner

class ListCreateUsersAPIView(ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        account = self.request.user.account
        return ExtendedUser.objects.filter(account=account)

class RetrieveUpdateDestroyUsersAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, UserPermissions]

    def get_queryset(self):
        account = self.request.user.account
        return ExtendedUser.objects.filter(account=account)

class RetrieveMeAPIView(RetrieveAPIView):
    serializer_class = serializers.UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return ExtendedUser.objects.get(id=self.request.user.id)
