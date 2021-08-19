from rest_framework.routers import DefaultRouter

from blogger_app import views

router = DefaultRouter()

router.register('blogs', views.BlogViewSet, basename='blogs')
router.register('tags', views.TagViewSet)
router.register('likes', views.LikesViewSet)
