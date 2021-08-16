from rest_framework.routers import DefaultRouter

from blogger_app import views

router = DefaultRouter()

router.register('blogs', views.BlogViewSet, basename='blogs')
