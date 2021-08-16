from rest_framework.routers import DefaultRouter

from hotels_api import views

router = DefaultRouter()

router.register('hotel', views.HotelViewSet, basename='hotels')
router.register('place', views.PlaceViewSet, basename='places')
router.register('hotels-db', views.HotelDbViewSet)
router.register('places-db', views.PlaceDbViewSet)