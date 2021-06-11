from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from rest_framework.documentation import include_docs_urls

schema_view = get_swagger_view(title='Polls API')
router = DefaultRouter()
# router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile',views.UserProfileViewSet,'profile')


# router.register('feed',views.UserProfileFeedViewSet)
urlpatterns = [
    # path('hello-view/', views.HelloApiView.as_view()),
    path('login/',views.UserLogInApiView.as_view()),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('swagger-docs/', schema_view),
    path('docs/', include_docs_urls(title='Polls API')),
    path('', include(router.urls)),
]
