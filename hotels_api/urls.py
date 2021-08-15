from rest_framework.routers import DefaultRouter

from hotels_api import views

router = DefaultRouter()

router.register('hotel', views.HotelViewSet, basename='hotels')
router.register('place', views.PlaceViewSet, basename='places')
router.register('hotel-db', views.HotelDbViewSet)
router.register('place-db', views.PlaceDbViewSet)
router.register('blogs', views.BlogViewSet, basename='blogs')
