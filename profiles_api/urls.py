from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views


router = DefaultRouter()
# router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile',views.UserProfileViewSet)
router.register('hotels',views.HotelViewSet)
router.register('places',views.PlaceViewSet)
# router.register('feed',views.UserProfileFeedViewSet)
urlpatterns = [
    # path('hello-view/', views.HelloApiView.as_view()),
    path('login/',views.UserLogInApiView.as_view()),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('', include(router.urls)),

]
