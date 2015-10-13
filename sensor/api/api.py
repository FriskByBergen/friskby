from rest_framework import generics

from sensor.models import *
from sensor.api.serializers import *

class MeasurementTypeList(generics.ListCreateAPIView):
    queryset = MeasurementType.objects.all()
    serializer_class = SnippetSerializer
