from .prediction_service_client import PredictionServiceClient

def notify_prediction_service_model_deleted(sender, instance, using, **kwargs):
    client = PredictionServiceClient(prediction_model=instance)

    client.stop_predicting()
