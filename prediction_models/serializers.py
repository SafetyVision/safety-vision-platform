from rest_framework import serializers
from .models import PredictionModel
from devices.serializers import DeviceRelatedField
from .prediction_service_client import PredictionServiceClient

class PredictionModelSerializer(serializers.ModelSerializer):
    device = DeviceRelatedField()
    number_captures = serializers.IntegerField(write_only=True)
    between_captures = serializers.IntegerField(write_only=True)

    class Meta:
        model = PredictionModel
        fields = [
            'infraction_type', 'device', 'is_predicting', 'training_state',
            'number_captures', 'between_captures', 'stream_delay',
        ]
        read_only_fields = ['is_predicting', 'training_state']
        extra_kwargs = {
            'number_captures': {'write_only': True},
            'between_captures': {'write_only': True},
            'stream_delay': {'write_only': True},
        }

    def validate(self, data):
        try:
            device = data.get('device')
            infraction_type = data.get('infraction_type')
            number_captures = data.get('number_captures')
            between_captures = data.get('between_captures')
            stream_delay = data.get('stream_delay')

            training_time = (between_captures / 1000) * number_captures

            if training_time > 600 or training_time <= 0:
                raise serializers.ValidationError()

            if stream_delay > 30 or stream_delay < 0:
                raise serializers.ValidationError()

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
            raise serializers.ValidationError('Invalid combination of device and infraction type or training config values')

        return super(PredictionModelSerializer, self).validate(data)

    def create(self, validated_data):
        number_captures = validated_data.pop('number_captures')
        between_captures = validated_data.pop('between_captures')


        model = PredictionModel.objects.create(**validated_data)

        client = PredictionServiceClient(model)
        client.train_new(
            number_captures=number_captures,
            between_captures=between_captures,
        )

        return model
