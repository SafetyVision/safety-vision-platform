from django.db import models
import boto3
from botocore.config import Config

class Device(models.Model):
    location = models.CharField(max_length=1000)
    stream_name = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def getStreamUrl(self):
        try:
            client = boto3.client(
                'kinesisvideo',
                config=Config(region_name='us-east-1'),
            )

            endpoint_response = client.get_data_endpoint(
                StreamName=self.stream_name,
                APIName='GET_HLS_STREAMING_SESSION_URL'
            )
            endpoint_url = endpoint_response['DataEndpoint']

            client = boto3.client(
                'kinesis-video-archived-media',
                endpoint_url=endpoint_url,
                config=Config(region_name='us-east-1')
            )
        
            stream_response = client.get_hls_streaming_session_url(
                StreamName=self.stream_name,
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
        return self.location
# Create your models here.
