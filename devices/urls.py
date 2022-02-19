from django.urls import path
from .views import RetrieveUpdateDeleteDeviceAPIView

urlpatterns = [
    path('<str:serial_number>', RetrieveUpdateDeleteDeviceAPIView.as_view())
]
