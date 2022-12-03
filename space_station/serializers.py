from rest_framework import serializers

from space_station.models import Instruction, Position, Station


class StationSerializer(serializers.ModelSerializer):
    """Serializer for `Station` model"""
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Station
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    """Serializer for `Position` model"""
    class Meta:
        model = Position
        fields = '__all__'


class InstructionSerializer(serializers.ModelSerializer):
    """Serializer for `Instruction` model"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Instruction
        fields = '__all__'
