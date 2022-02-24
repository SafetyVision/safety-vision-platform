from django.urls import path
from .views import ListCreateInfractionTypesAPIView, RetrieveUpdateDestroyInfractionTypesAPIView

urlpatterns = [
    path('', ListCreateInfractionTypesAPIView.as_view()),
    path('<int:pk>', RetrieveUpdateDestroyInfractionTypesAPIView.as_view()),
]
