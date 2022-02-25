from rest_framework import serializers
from .models import PredictionModel
from devices.models import Device

class PredictionModelSerializer(serializers.ModelSerializer):
    serial_number = serializers.CharField(write_only=True)

    class Meta:
        model = PredictionModel
        fields = ['id', 'infraction_type', 'serial_number', 'device']
        read_only_fields = ['id', 'device']

    def validate(self, data):
        try:
            device = data.get('serial_number')
            infraction_type = data.get('infraction_type')
            request_user = self.context['request'].user

            if infraction_type.account != request_user.account:
                raise serializers.ValidationError()

            devices = Device.objects.filter(location__account=request_user.account)
            device = devices.get(serial_number=device)

            models = PredictionModel.objects.filter(device=device, infraction_type=infraction_type)
            if models:
                raise serializers.ValidationError()
        except:
            raise serializers.ValidationError('Invalid combination of device and infraction type')

        return super(PredictionModelSerializer, self).validate(data)

    def create(self, validated_data):
        return PredictionModel.objects.create(
            device = Device.objects.get(serial_number=validated_data['serial_number']),
            infraction_type = validated_data['infraction_type'],
        )
