from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

# from rest_framework.schemas import get_schema_view
# from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

# router = DefaultRouter()
# router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')


# router.register('feed',views.UserProfileFeedViewSet)
urlpatterns = [
    # path('hello-view/', views.HelloApiView.as_view()),
    path('login/',views.UserLogInApiView.as_view()),
    # path('hello/', views.HelloView.as_view(), name='hello'),
    # path('docs/', include_docs_urls(title='Polls API')),
    path('register/',views.UserRegisterViewSet.as_view()),
    # path('docs/', schema_view, name="docs"),
]
