from django.db import models
import boto3
from botocore.config import Config
from locations.models import Location

class Device(models.Model):
    serial_number = models.CharField(max_length=1000, unique=True, default='')
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name='devices',
    )
    description = models.CharField(max_length=255, default='')
    stream_arn = models.CharField(max_length=1000, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def getStreamUrl(self):
        try:
            client = boto3.client(
                'kinesisvideo',
                config=Config(region_name='us-east-1'),
            )

            endpoint_response = client.get_data_endpoint(
                StreamARN=self.stream_arn,
                APIName='GET_HLS_STREAMING_SESSION_URL'
            )
            endpoint_url = endpoint_response['DataEndpoint']

            client = boto3.client(
                'kinesis-video-archived-media',
                endpoint_url=endpoint_url,
                config=Config(region_name='us-east-1')
            )

            stream_response = client.get_hls_streaming_session_url(
                StreamARN=self.stream_arn,
                PlaybackMode='LIVE',
                ContainerFormat='FRAGMENTED_MP4',
                DiscontinuityMode='ALWAYS',
                DisplayFragmentTimestamp='NEVER',
                Expires=43100,
                MaxMediaPlaylistFragmentResults=3
            )
        except:
            return None

        return stream_response['HLSStreamingSessionURL']

    def __str__(self):
        if self.description:
            return self.description
        return f'Unassigned device with serial number: {self.serial_number}'
