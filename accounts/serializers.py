from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Account
from users.models import ExtendedUser

class CreateAccountSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Account
        fields = ['account_name', 'login_identifier', 'users']

    def validate_users(self, users):
        if len(users) != 1:
            raise serializers.ValidationError("Must include exactly one user when registering a new account")
        return users

    def create(self, validated_data):
        user = validated_data.pop('users', None)[0]
        account = Account.objects.create(**validated_data)
        password = user.pop('password')
        user = ExtendedUser.objects.create(**user, account=account)
        user.set_password(password)
        user.save()

        return account

class GetUpdateDeleteAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'login_identifier']
