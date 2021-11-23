from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Account
from users.models import ExtendedUser

class CreateAccountSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Account
        fields = ['account_name', 'login_identifier', 'users']

    def create(self, validated_data):
        user = validated_data.pop('users', None)
        if user and user[0] and len(user) == 1:
            account = Account.objects.create(**validated_data)

            user = user[0]
            password = user.pop('password')
            user = ExtendedUser.objects.create(**user, account=account)
            user.set_password(password)
            user.save()

            return account
        else:
            serializers.ValidationError("Must provide exactly one valid user when creating an account")

class GetUpdateDeleteAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'login_identifier']