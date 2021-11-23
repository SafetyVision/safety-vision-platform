from rest_framework.serializers import ModelSerializer
from .models import ExtendedUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        request_user = self.context['request'].user
        user = ExtendedUser.objects.create(**validated_data, account=request_user.account)
        user.set_password(password)
        user.save()
        return user
