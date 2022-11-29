from rest_framework import serializers

from space_station.models import Position, Station


class StationSerializer(serializers.ModelSerializer):

    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Station
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'