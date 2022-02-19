from django.urls import path
from .views import ListCreateLocationAPIView, RetrieveUpdateDeleteLocationAPIView

urlpatterns = [
    path('', ListCreateLocationAPIView.as_view()),
    path('<int:pk>', RetrieveUpdateDeleteLocationAPIView.as_view())
]
