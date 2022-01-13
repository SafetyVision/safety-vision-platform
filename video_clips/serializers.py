from rest_framework import serializers
from .models import VideoClip

class VideoClipSerializer(serializers.ModelSerializer):
  file = serializers.CharField(source='__str__', max_length=1000)

  class Meta:
    model = VideoClip
    fields = ['file']
