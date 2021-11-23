from rest_framework import generics
from .models import TestModel
from .serializers import TestModelSerializer
from rest_framework.permissions import IsAuthenticated


class ListTestModel(generics.ListCreateAPIView):
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
    permission_classes = [IsAuthenticated]


class DetailTestModel(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
    permission_classes = [IsAuthenticated]
