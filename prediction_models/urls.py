from django.urls import path
from .views import CreatePredictionModelAPIView, RetrieveDeletePredictionModelAPIView

urlpatterns = [
    path('', CreatePredictionModelAPIView.as_view()),
    path('<str:device>/<int:infraction_type>', RetrieveDeletePredictionModelAPIView.as_view())
]
