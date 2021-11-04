from rest_framework import generics

from .models import Test
from .serializers import TestSerializer


class ListTest(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class DetailTest(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer