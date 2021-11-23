from django.urls import path
from .views import GetUpdateDeleteAccountAPIView, ListAccountAPIView, CreateAccountAPIView

urlpatterns = [
    path('', ListAccountAPIView.as_view()),
    path('register', CreateAccountAPIView.as_view()),
    path('<int:pk>', GetUpdateDeleteAccountAPIView.as_view())
]
