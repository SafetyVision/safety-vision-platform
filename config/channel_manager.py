from django_eventstream.channelmanager import DefaultChannelManager

class EventChannelManager(DefaultChannelManager):
    def can_read_channel(self, user, channel):
        if user and channel == f'account_{user.account.id}_events':
            return True
        return False
