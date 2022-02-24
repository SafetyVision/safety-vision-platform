from django.urls import path
from .views import ListCreateInfractionTypesAPIView

urlpatterns = [
    path('', ListCreateInfractionTypesAPIView.as_view()),
    # path('<int:pk>', views.RetrieveUpdateDestroyInfractionTypesAPIView.as_view())
]
