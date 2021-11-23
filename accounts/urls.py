from django.urls import path
from .views import ListCreateAccountAPIView, GetUpdateDeleteAccountAPIView

urlpatterns = [
    path('', ListCreateAccountAPIView.as_view()),
    path('<int:pk>', GetUpdateDeleteAccountAPIView.as_view())
]
