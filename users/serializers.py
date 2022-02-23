from rest_framework.serializers import ModelSerializer, ValidationError
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import ExtendedUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = ('id', 'first_name', 'last_name', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')

        if password:
            user = ExtendedUser(**data)
            errors = {}
            try:
                django_validate_password(password, user)
            except DjangoValidationError as password_error:
                errors['password'] = list(password_error.messages)

            if errors:
                raise ValidationError(errors)

        return super(UserSerializer, self).validate(data)

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
        if validated_data['email']:
            validated_data['username'] = validated_data['email']

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance

class UserMeSerializer(ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = ('id', 'first_name', 'last_name', 'email', 'account', 'isOwner')
