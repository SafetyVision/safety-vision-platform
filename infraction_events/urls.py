from django.urls import path
from .views import ListCreateInfractionEventsAPIView, GetDeleteInfractionEventsAPIView, PostInfractionEventsAPIView

urlpatterns = [
    path('', ListCreateInfractionEventsAPIView.as_view()),
    path('<int:pk>', GetDeleteInfractionEventsAPIView.as_view()),
    path('create', PostInfractionEventsAPIView.as_view()),
]
