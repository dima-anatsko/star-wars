from django.apps import AppConfig


class SpaceStationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'space_station'

    def ready(self):
        import space_station.signals
