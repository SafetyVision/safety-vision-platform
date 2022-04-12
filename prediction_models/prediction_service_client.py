import requests
from config.settings import DEBUG

def mock_post(*args, **kwargs):
    print(args, kwargs)
    return {}

class PredictionServiceClient:
    def __init__(self, prediction_model):
        self.url = 'http://ec2-34-229-159-65.compute-1.amazonaws.com:5000'
        self.kvs_stream_arn = prediction_model.device.stream_arn
        self.body = {
            'device_serial_number': prediction_model.device.serial_number,
            'infraction_type_id': prediction_model.infraction_type.id,
            'kvs_arn': self.kvs_stream_arn,
            'stream_delay': prediction_model.stream_delay,
        }
        if DEBUG:
            requests.post = mock_post

    def train_new(self, number_captures, between_captures):
        body = self.body.copy()
        body['num_captures'] = number_captures
        body['between_captures'] = between_captures / 1000 # Cameron wants this in seconds
        try:
            requests.post(url=f'{self.url}/train_new', json=body, timeout=0.01)
            return True
        except:
            return True

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
