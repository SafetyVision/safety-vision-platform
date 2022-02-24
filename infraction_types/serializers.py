from rest_framework import serializers
from .models import InfractionType

class InfractionTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfractionType
        fields = ['id', 'infraction_type_name', 'created_at']
        read_only_fields = ['id', 'created_at']
