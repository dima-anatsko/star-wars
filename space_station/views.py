from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from space_station.models import Position, Station
from space_station.serializers import PositionSerializer, StationSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get', 'post'], detail=True)
    def state(self, request, pk=None):
        if request.method == 'GET':
            return self._get_state(request, pk)
        return self._post_state(request, pk)

    @staticmethod
    def _get_state(request, station_pk):
        position = get_object_or_404(Position, station_id=station_pk)
        serializer = PositionSerializer(position)
        return Response(serializer.data)

    @staticmethod
    def _post_state(request, station_pk):
        position = get_object_or_404(Position, station_id=station_pk)
        #  TODO update state, validate_data
        serializer = PositionSerializer(position)
        return Response(serializer.data)
