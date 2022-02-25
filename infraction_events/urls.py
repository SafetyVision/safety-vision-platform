from django.urls import path
from .views import ListInfractionEventsAPIView, GetInfractionEventsAPIView, PostInfractionEventsAPIView

urlpatterns = [
    path('', ListInfractionEventsAPIView.as_view()),
    path('<int:pk>', GetInfractionEventsAPIView.as_view()),
    path('create', PostInfractionEventsAPIView.as_view()),
]
