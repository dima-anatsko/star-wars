from rest_framework.routers import DefaultRouter

from space_station.views import StationViewSet


router = DefaultRouter()
router.register(r'stations', StationViewSet, basename='stations')

urlpatterns = router.urls
