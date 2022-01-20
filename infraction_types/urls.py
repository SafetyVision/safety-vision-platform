from django.urls import path
from .views import CreateInfractionTypeAPIView, ListInfractionTypesAPIView

urlpatterns = [
    path('', ListInfractionTypesAPIView.as_view()),
    path('create', CreateInfractionTypeAPIView.as_view()),
    # path('<int:pk>', views.RetrieveUpdateDestroyInfractionTypesAPIView.as_view())
]
