from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Station(models.Model):
    """Class for creating space stations."""

    class Status(models.TextChoices):
        BROKEN = 'BR', _('broken')
        RUNNING = 'RG', _('running')

    name = models.CharField(
        verbose_name=_('Name of station'),
        max_length=100,
        unique=True,
    )
    status = models.CharField(
        verbose_name=_('Station status'),
        editable=False,
        max_length=2,
        choices=Status.choices,
        default=Status.RUNNING,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Start date'),
        editable=False,
        auto_now_add=True,
    )
    broke_at = models.DateTimeField(
        verbose_name=_('Date of breakdown'),
        editable=False,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Station')
        verbose_name_plural = _('Stations')

    def __str__(self) -> str:
        return self.name.__str__()


class Position(models.Model):
    """Class for saving position of space station."""

    station = models.OneToOneField(Station, on_delete=models.CASCADE)
    x = models.IntegerField(verbose_name=_('X-axis coordinate'), default=100)
    y = models.IntegerField(verbose_name=_('Y-axis coordinate'), default=100)
    z = models.IntegerField(verbose_name=_('Z-axis coordinate'), default=100)

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')

    def __str__(self) -> str:
        return (
            f'Position of {self.station.name} is ({self.x}, {self.y}, {self.z})'
        )


class Instruction(models.Model):
    """Class for creating instructions for space stations."""

    class Axis(models.TextChoices):
        X = 'X', 'x'
        Y = 'Y', 'y'
        Z = 'Z', 'z'

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='instructions'
    )
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name='instructions'
    )
    axis = models.CharField(
        verbose_name=_('Axis'), max_length=1, choices=Axis.choices
    )
    distance = models.IntegerField(verbose_name=_('Distance'))

    class Meta:
        verbose_name = _('Instruction')
        verbose_name_plural = _('Instructions')

    def __str__(self) -> str:
        return (
            f'Instruction of {self.user.username} to {self.station.name} '
            f'{self.axis}={self.distance}'
        )
