from rest_framework import serializers
from .models import Test

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'description',
        )
        model = Test