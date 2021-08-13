from rest_framework.routers import DefaultRouter

from trips_api import views

router = DefaultRouter()

router.register('trips', views.TripViewSet, basename='trips')
