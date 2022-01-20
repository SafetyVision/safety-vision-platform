from rest_framework import serializers
from .models import InfractionType

class ListInfractionTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfractionType
        # fields = ['id', 'infraction_type_name', 'device_id', 'created_at']
        fields = ['id', 'infraction_type_name', 'created_at']
class CreateInfractionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfractionType
        fields = ['infraction_type_name']

