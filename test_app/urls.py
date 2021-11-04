from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListTestModel.as_view()),
    path('<int:pk>/', views.DetailTestModel.as_view()),
]
