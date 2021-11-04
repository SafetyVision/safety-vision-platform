from rest_framework import generics

from .models import TestModel
from .serializers import TestModelSerializer


class ListTestModel(generics.ListCreateAPIView):
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer


class DetailTestModel(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
