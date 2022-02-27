from django.apps import AppConfig
from django.db.models.signals import pre_delete
from .receivers import notify_prediction_service_model_deleted


class PredictionModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction_models'

    def ready(self):
        pre_delete.connect(notify_prediction_service_model_deleted, sender='prediction_models.PredictionModel')
