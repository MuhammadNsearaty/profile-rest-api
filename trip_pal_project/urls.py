"""trip_pal_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from blogger_app.urls import router as blogger_router
from patches.routers import DefaultRouter
from planning_app.urls import router as planning_router
from profiles_app.urls import router as profile_router
from trip_pal_project import settings

router = DefaultRouter()
router.extend(profile_router)
router.extend(planning_router)
router.extend(blogger_router)

schema_view = get_schema_view(
    openapi.Info(
        title="TripPal",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), )
docs_urls = [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path(settings.BASE_API_URL, include(router.urls + docs_urls)),
]
