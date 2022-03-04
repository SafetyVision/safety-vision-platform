from rest_framework import serializers
from .models import Location
from devices.serializers import DeviceSerializer

class LocationSerializerForInfractionEvents(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'description']

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
