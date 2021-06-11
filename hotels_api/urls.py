from django.urls import path, include
from hotels_api import views
from rest_framework.routers import DefaultRouter




router = DefaultRouter()
router.register('hotel',views.HotelViewSet,basename='hotels')
router.register('place',views.PlaceViewSet,basename='places')

urlpatterns =[
    path('', include(router.urls)),
]
