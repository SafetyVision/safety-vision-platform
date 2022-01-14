from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import VideoClip
from . import serializers

class GetDeleteVideoClipView(RetrieveDestroyAPIView):
  queryset = VideoClip.objects.all()
  permission_classes = [IsAuthenticated]
  serializer_class = serializers.VideoClipSerializer
