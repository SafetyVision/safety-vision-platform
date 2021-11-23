from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from . import models

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data.pop('userprofile', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        request_user = self.context['request'].user
        models.UserProfile.objects.create(user=user, account=request_user.userprofile.account)

        user.set_password(password)
        user.save()
        return user
