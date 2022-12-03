import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.generics import get_object_or_404

from space_station.models import Instruction, Position, Station


@receiver(post_save, sender=Station)
def create_position(sender, instance: Station, **kwargs) -> None:
    """After creating the station, we create a position"""
    if not Position.objects.filter(station_id=instance.id).exists():
        position = Position(station=instance)
        position.save()


@receiver(post_save, sender=Instruction)
def apply_instruction(sender, instance: Instruction, **kwargs) -> None:
    """
    After creating the instruction, we apply them to a position of the station
    """
    position = get_object_or_404(Position, station=instance.station)
    new_axis_value = getattr(position, instance.axis) + instance.distance
    setattr(position, instance.axis, new_axis_value)
    position.save()

    # checking the correct station position
    if position.station.status == Station.Status.RUNNING and new_axis_value < 0:
        position.station.status = Station.Status.BROKEN
        position.station.broke_at = datetime.datetime.now()
        position.station.save()
