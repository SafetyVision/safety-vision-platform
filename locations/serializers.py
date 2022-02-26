from rest_framework import serializers
from .models import Location
from devices.serializers import DeviceSerializer

class LocationRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return instance.description

    def to_internal_value(self, data):
        return Location.objects.get(id=data)

    def get_queryset(self):
        return Location.objects.all()

class LocationSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'description', 'devices']
        read_only_fields = ['id', 'devices']

    def create(self, validated_data):
        account = self.context['request'].user.account
        return Location.objects.create(
            **validated_data,
            account=account,
        )
