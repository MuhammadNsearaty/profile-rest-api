from rest_framework.routers import DefaultRouter

from profiles_app import views

router = DefaultRouter()

router.register('login', views.UserLoginApiView, basename='login')
router.register('register', views.UserRegisterViewSet, basename='register')
router.register('users', views.UserProfilesApiView, basename='users')
router.register('devices', views.DevicesViewSet, basename='devices')
