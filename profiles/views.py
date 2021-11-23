from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from profiles.models import UserProfile
from . import serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class ListCreateUsersAPIView(ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.username == "admin":
            return User.objects.all()
        account = self.request.user.userprofile.account
        return User.objects.filter(userprofile__in=UserProfile.objects.filter(account=account))

class RetrieveUpdateDestroyUsersAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account = self.request.user.userprofile.account
        return User.objects.filter(userprofile__in=UserProfile.objects.filter(account=account))
