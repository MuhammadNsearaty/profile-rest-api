from django.urls import path, include
from hotels_api import views
from rest_framework.routers import DefaultRouter
from trips_api import views




router = DefaultRouter()
router.register('trips',views.TripViewSet,basename='trips')
urlpatterns =[
    path('',include(router.urls)),
]
