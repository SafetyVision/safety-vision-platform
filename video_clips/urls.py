from django.urls import path
from .views import GetDeleteVideoClipView

urlpatterns = [path('<int:pk>', GetDeleteVideoClipView.as_view())]
