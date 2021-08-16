"""profiles_project URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from hotels_api.urls import router as hotel_router
from patches.routers import DefaultRouter
from profiles_api.urls import router as profile_router
from profiles_project import settings
from trips_api.urls import router as trip_router
from blogger_app.urls import router as blogger_router

router = DefaultRouter()
router.extend(profile_router)
router.extend(hotel_router)
router.extend(trip_router)
router.extend(blogger_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(settings.BASE_API_URL, include(router.urls)),
]
