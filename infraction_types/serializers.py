from rest_framework import serializers
from .models import InfractionType
import requests

class ListInfractionTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfractionType
        fields = ['id', 'infraction_type_name', 'device', 'created_at']

class CreateInfractionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfractionType
        fields = ['infraction_type_name', 'device']

    def create(self, validated_data):
        request_account_id = self.context['request'].user.account.id
        infraction_type = InfractionType.objects.create(**validated_data)

        url = "http://ec2-3-80-89-68.compute-1.amazonaws.com:5000/train_new"
        json = {
            'kvs_arn': infraction_type.device.stream_arn,
            'infraction_type': infraction_type.id,
            'account_id': request_account_id,
            'location': infraction_type.device.id,
        }

        try:
            requests.post(url=url, json=json, timeout=0.01)
        except:
            pass

        return infraction_type
