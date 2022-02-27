from django.urls import path
from .views import (
    RetrieveUpdateDeleteDeviceAPIView,
    ListCreatePredictionModelAPIView,
    RetrieveDeletePredictionModelAPIView,
    StartCommitInfraction,
    DoneCommitInfraction,
    StartNotCommitInfraction,
    DoneNotCommitInfraction,
    TrainingComplete,
    NeedsRetraining,
    StartPredicting,
    PausePredicting
)

urlpatterns = [
    path('<str:serial_number>', RetrieveUpdateDeleteDeviceAPIView.as_view()),
    path('<str:serial_number>/infraction_types/', ListCreatePredictionModelAPIView.as_view()),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>',
        RetrieveDeletePredictionModelAPIView.as_view()
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/start_commit',
        StartCommitInfraction.as_view()
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/done_commit',
        DoneCommitInfraction.as_view()
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/start_not_commit',
        StartNotCommitInfraction.as_view(),
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/done_not_commit',
        DoneNotCommitInfraction.as_view(),
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/training_complete',
        TrainingComplete.as_view(),
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/needs_retraining',
        NeedsRetraining.as_view(),
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/start_predict',
        StartPredicting.as_view(),
    ),
    path(
        '<str:serial_number>/infraction_types/<int:infraction_type>/stop_predict',
        PausePredicting.as_view(),
    ),
]
