from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateUsersAPIView.as_view()),
    path('<int:pk>', views.RetrieveUpdateDestroyUsersAPIView.as_view())
]
