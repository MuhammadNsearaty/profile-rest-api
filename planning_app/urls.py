from rest_framework.routers import DefaultRouter

from planning_app import views

router = DefaultRouter()

# router.register('hotel', views.HotelViewSet, basename='hotels')
# router.register('place', views.PlaceViewSet, basename='places')
router.register('hotels-db', views.HotelDbViewSet, basename='hotels')
router.register('places-db', views.PlaceDbViewSet, basename='places')
router.register('places-review', views.PlacesReviewsViewSet, basename='places_review')
router.register('trips', views.TripViewSet, basename='trips')
