# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from rest_framework import generics, status
from rest_framework.response import Response

from measurement.models import Measurement, Sensor
from measurement.serializers import MeasurementSerializer, SensorSerializer


class SensorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        sensor = Sensor.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description')
        )
        return Response(SensorSerializer(sensor).data, status=status.HTTP_201_CREATED)

class SensorRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    # def patch(self, request, pk):
    #     sensor = self.get_object()
    #     serializer = SensorSerializer(sensor, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeasurementCreateAPIView(generics.CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer