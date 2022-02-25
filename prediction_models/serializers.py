from rest_framework import serializers
from .models import PredictionModel
from devices.serializers import DeviceRelatedField

class PredictionModelSerializer(serializers.ModelSerializer):
    device = DeviceRelatedField()

    class Meta:
        model = PredictionModel
        fields = ['infraction_type', 'device']

    def validate(self, data):
        try:
            device = data.get('device')
            infraction_type = data.get('infraction_type')

            account = self.context['request'].user.account
            if device.location.account != account or infraction_type.account != account:
                raise serializers.ValidationError()

            models = PredictionModel.objects.filter(device=device, infraction_type=infraction_type)
            if models:
                raise serializers.ValidationError()
        except:
            raise serializers.ValidationError('Invalid combination of device and infraction type')

        return super(PredictionModelSerializer, self).validate(data)
