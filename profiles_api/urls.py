from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views


router = DefaultRouter()
# router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile',views.UserProfileViewSet,'Profile')
router.register('hotels',views.HotelViewSet)
# router.register('feed',views.UserProfileFeedViewSet)
urlpatterns = [
    # path('hello-view/', views.HelloApiView.as_view()),
    path('login/',views.UserLoginView.as_view()),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),

]
