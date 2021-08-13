from rest_framework.routers import DefaultRouter

from profiles_api import views

router = DefaultRouter()

router.register('login', views.UserLoginApiView, basename='login')
router.register('register', views.UserRegisterViewSet, basename='register')
router.register('devices', views.DevicesViewSet)
