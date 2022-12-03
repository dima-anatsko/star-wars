from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from space_station.models import Position, Station
from space_station.serializers import (
    InstructionSerializer,
    PositionSerializer,
    StationSerializer,
)


@extend_schema_view(
    list=extend_schema(description='Get list of stations'),
    retrieve=extend_schema(description='Get information of the station'),
    create=extend_schema(description='Create the station'),
    update=extend_schema(description='Update the station'),
    partial_update=extend_schema(description='Partial update the station'),
    destroy=extend_schema(description='Delete the station'),
)
class StationViewSet(viewsets.ModelViewSet):
    """View to represent the station"""
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=InstructionSerializer,
        responses={201: PositionSerializer},
        methods=['POST'],
        description='Move the station along a given axis by a certain distance',
    )
    @extend_schema(
        responses={200: PositionSerializer},
        description='Get the position of the station',
        methods=['GET'],
    )
    @action(methods=['get', 'post'], detail=True)
    def state(self, request, pk: int = None) -> Response:
        """Provides methods for displaying and changing the station position"""
        if request.method == 'GET':
            return self._get_state(request, pk)
        return self._post_state(request, pk)

    @staticmethod
    def _get_state(request, station_pk: int) -> Response:
        """Return the `Position` of the `Station`"""
        position = get_object_or_404(Position, station_id=station_pk)
        serializer = PositionSerializer(position)
        return Response(serializer.data)

    def _post_state(self, request, station_pk: int) -> Response:
        """Create `Instruction, move `Station` and return new `Position`"""
        self._create_instruction(request)
        position = get_object_or_404(Position, station_id=station_pk)
        serializer = PositionSerializer(position)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _create_instruction(request) -> None:
        """Create `Instruction`"""
        instruction = InstructionSerializer(
            data=request.data,
            context={'request': request},
        )
        instruction.is_valid(raise_exception=True)
        instruction.save()
