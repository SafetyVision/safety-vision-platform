import requests
from config.settings import DEBUG

def mock_post(*args, **kwargs):
    print(args, kwargs)
    return {}

class PredictionServiceClient:
    def __init__(self, device, infraction_type):
        self.url = 'http://ec2-3-80-89-68.compute-1.amazonaws.com:5000'
        self.kvs_stream_arn = device.stream_arn
        self.body = {
            'device_serial_number': device.serial_number,
            'infraction_type_id': infraction_type.id,
        }
        if DEBUG:
            requests.post = mock_post

    def train_new(self, number_captures, between_captures, stream_delay):
        body = self.body.copy()
        body['num_captures'] = number_captures
        body['between_captures'] = between_captures / 1000 # Cameron wants this is seconds
        body['stream_delay'] = stream_delay
        try:
            requests.post(url=f'{self.url}/train_new', json=body)
            return True
        except:
            raise False

    def start_positive(self):
        try:
            requests.post(url=f'{self.url}/start_positive', json=self.body)
            return True
        except:
            raise False

    def start_negative(self):
        try:
            requests.post(url=f'{self.url}/start_negative', json=self.body)
            return True
        except:
            raise False

    def stop_predicting(self):
        try:
            requests.post(url=f'{self.url}/stop_predicting', json=self.body)
            return True
        except:
            raise False

    def restart_predicting(self):
        try:
            requests.post(url=f'{self.url}/restart_predicting', json=self.body)
            return True
        except:
            raise False
