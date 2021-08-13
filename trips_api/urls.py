from trips_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('trips', views.TripViewSet, basename='trips')
