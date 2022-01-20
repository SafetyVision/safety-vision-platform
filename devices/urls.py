from django.urls import path
from .views import GetUpdateDeleteDeviceAPIView, ListDeviceAPIView, CreateDeviceAPIView

urlpatterns = [
    path('', ListDeviceAPIView.as_view()),
    path('create', CreateDeviceAPIView.as_view()),
    path('<int:pk>', GetUpdateDeleteDeviceAPIView.as_view())
]