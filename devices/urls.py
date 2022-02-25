from django.urls import path
from .views import (
    RetrieveUpdateDeleteDeviceAPIView,
    ListCreatePredictionModelAPIView,
    RetrieveDeletePredictionModelAPIView,
    StartCommitFirstInfraction,
    DoneCommitFirstInfraction
)

urlpatterns = [
    path('<str:serial_number>', RetrieveUpdateDeleteDeviceAPIView.as_view()),
    path('<str:serial_number>/infraction_types/', ListCreatePredictionModelAPIView.as_view()),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>',
        RetrieveDeletePredictionModelAPIView.as_view()
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/start_commit_1',
        StartCommitFirstInfraction.as_view()
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/done_commit_1',
        DoneCommitFirstInfraction.as_view()
    ),
]
