from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from space_station.models import Instruction, Position, Station


class InstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'station_name', 'axis', 'distance')
    search_fields = ('id', 'user__name', 'id', 'station__name')
    list_select_related = True

    @admin.display(description=_('User name'))
    def user_name(self, obj: Instruction) -> str:
        return f'{obj.user.username}'

    @admin.display(description=_('Station name'))
    def station_name(self, obj: Instruction) -> str:
        return f'{obj.station.name}'


class PositionInline(admin.TabularInline):
    model = Position
    fields = ('x', 'y', 'z')
    max_num = 1


class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'created_at', 'broke_at')
    inlines = (PositionInline, )


admin.site.register(Instruction, InstructionAdmin)
admin.site.register(Station, StationAdmin)
