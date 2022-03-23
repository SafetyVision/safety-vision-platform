from django_eventstream.channelmanager import DefaultChannelManager
from infraction_types.models import InfractionType
from devices.models import Device
from prediction_models.models import PredictionModel

class EventChannelManager(DefaultChannelManager):
    def can_read_channel(self, user, channel):
        if user and channel == f'account_{user.account.id}_events':
            return True

        try:
            parsed_channel = channel.split('_')
            serial_number = parsed_channel[0]
            infraction_type_id = int(parsed_channel[1])

            infraction_type = InfractionType.objects.get(id=infraction_type_id)
            device = Device.objects.get(serial_number=serial_number)
            prediction_model = PredictionModel.objects.get(device=device, infraction_type=infraction_type)

            if prediction_model.infraction_type.account.id == user.account.id:
                return True
        except:
            pass

        try:
            parsed_channel = channel.split('_')
            if len(parsed_channel) == 3 and parsed_channel[0] == 'device' and parsed_channel[2] == 'events':
                return True
        except:
            pass

        return False
