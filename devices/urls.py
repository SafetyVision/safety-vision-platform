from django.urls import path
from .views import RetrieveUpdateDeleteDeviceAPIView, ListCreatePredictionModelAPIView, RetrieveDeletePredictionModelAPIView

urlpatterns = [
    path('<str:serial_number>', RetrieveUpdateDeleteDeviceAPIView.as_view()),
    path('<str:serial_number>/infraction_types/', ListCreatePredictionModelAPIView.as_view()),
    path('<str:serial_number>/infraction_types/<int:infraction_type>', RetrieveDeletePredictionModelAPIView.as_view())
]
