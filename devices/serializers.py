from asyncio import sleep
from socket import timeout
from rest_framework import serializers
from .models import Device
import boto3
from botocore.config import Config

class CreateDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['serial_number', 'location']

    def create(self, validated_data):
        region = 'us-east-1'
        stream_name='SafetyVision-VS-'+validated_data['serial_number']
        def getStreamEndpoint(client):
            return  client.get_data_endpoint(
                        StreamName=stream_name,
                        APIName='GET_HLS_STREAMING_SESSION_URL'
                    )
        client = boto3.client(
            'kinesisvideo',
            config=Config(region_name=region),
        )
        try:
            stream = client.describe_stream(
                        StreamName=stream_name
                    )
            streamArn = stream['StreamInfo']['StreamARN']
        except:
            print("-------------------------------------\n\
                no stream with name: " + stream_name +\
                "\nCreating new stream...")
            stream = client.create_stream(
                StreamName=stream_name,
                DataRetentionInHours=1
            )
            streamArn = stream['StreamARN']

        endpoint_response = getStreamEndpoint(client)
        endpoint_url = endpoint_response['DataEndpoint']
        
        counter = 0
        timeout = 60
        while counter < timeout:
            try:
                client2 = boto3.client(
                    'kinesis-video-archived-media',
                    endpoint_url=endpoint_url,
                    config=Config(region_name=region)
                )
            
                client2.get_hls_streaming_session_url(
                    StreamName=stream_name,
                    PlaybackMode='LIVE',
                    ContainerFormat='FRAGMENTED_MP4',
                    DiscontinuityMode='ALWAYS',
                    DisplayFragmentTimestamp='NEVER',
                    Expires=43100,
                    MaxMediaPlaylistFragmentResults=3
                )
                break
            except:
                counter += 1
                sleep(1)
                
        if counter == timeout:
            client.delete_stream(
                    StreamARN=streamArn
                )
            raise serializers.ValidationError("Device [" + validated_data['serial_number'] + "] not streaming")

        device = Device(
            **validated_data,
            stream_arn=streamArn
        )
        device.save()

        return device

class DeviceSerializer(serializers.ModelSerializer):
    stream_url = serializers.CharField(source='getStreamUrl', max_length=1000)

    class Meta:
        model = Device
        fields = ['id', 'serial_number', 'location','stream_url']
