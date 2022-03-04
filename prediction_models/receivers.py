from .prediction_service_client import PredictionServiceClient

def notify_prediction_service_model_deleted(sender, instance, using, **kwargs):
    client = PredictionServiceClient(
        device=instance.device,
        infraction_type=instance.infraction_type
    )

    client.stop_predicting()
