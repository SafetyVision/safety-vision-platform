from django.urls import path
from . import views

urlpatterns = [
  path('', views.CreateAccountAPIView.as_view()),
  path('<int:pk>', views.GetUpdateDeleteAccountAPIView.as_view())
]
