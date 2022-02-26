from rest_framework import serializers
from .models import PredictionModel
from devices.serializers import DeviceRelatedField

class PredictionModelSerializer(serializers.ModelSerializer):
    device = DeviceRelatedField()

    class Meta:
        model = PredictionModel
        fields = ['infraction_type', 'device', 'is_predicting', 'training_state']
        read_only_fields = ['is_predicting', 'training_state']

    def validate(self, data):
        try:
            device = data.get('device')
            infraction_type = data.get('infraction_type')

            request = self.context['request']
            account = request.user.account
            if device.location.account != account or infraction_type.account != account:
                raise serializers.ValidationError()

            if request.method == 'POST':
                models = PredictionModel.objects.filter(device=device, infraction_type=infraction_type)
                if models:
                    raise serializers.ValidationError()
            else:
                PredictionModel.objects.get(device=device, infraction_type=infraction_type)
        except:
            raise serializers.ValidationError('Invalid combination of device and infraction type')

        return super(PredictionModelSerializer, self).validate(data)
