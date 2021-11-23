from rest_framework.serializers import ModelSerializer
from .models import ExtendedUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = ('id', 'first_name', 'last_name', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        request_user = self.context['request'].user
        user = ExtendedUser.objects.create(
            **validated_data,
            account=request_user.account,
            username=validated_data['email'],
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        ExtendedUser.objects.filter(id=instance.id).update(**validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return ExtendedUser.objects.get(id=instance.id)

class UserMeSerializer(ModelSerializer):
        class Meta:
            model = ExtendedUser
            fields = ('id', 'first_name', 'last_name', 'email', 'account')
