from rest_framework import serializers
from profiles.serializers import UserSerializer
from . import models
from profiles.models import UserProfile
from django.contrib.auth.models import User

class CreateAccountSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = models.Account
        fields = ['account_name', 'login_identifier', 'users']

    def create(self, validated_data):
        user = validated_data.pop('users', None)
        if user and user[0]:
            account = models.Account.objects.create(**validated_data)
            account.save()
            user = user[0]
            password = user.pop('password')
            user = User.objects.create_user(**user)
            user.set_password(password)
            user.save()

            userprofile = UserProfile.objects.create(user=user, account=account)
            userprofile.save()

            return account
        else:
            serializers.ValidationError("Must provide exactly one valid user when creating an account")

class GetUpdateDeleteAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ['id', 'account_name', 'login_identifier']
