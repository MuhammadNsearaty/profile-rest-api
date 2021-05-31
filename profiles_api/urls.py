from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

schema_view = get_swagger_view(title='Polls API')
router = DefaultRouter()
# router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile',views.UserProfileViewSet,'Profile')
router.register('hotels',views.HotelViewSet)
router.register('places',views.PlaceViewSet)
# router.register('feed',views.UserProfileFeedViewSet)
urlpatterns = [
    # path('hello-view/', views.HelloApiView.as_view()),
<<<<<<< HEAD
    path('login/',views.UserLogInApiView.as_view()),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('swagger-docs/', schema_view),
    path('docs/', include_docs_urls(title='Polls API')),
=======
    path('login/',views.UserLoginView.as_view()),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
>>>>>>> master
    path('', include(router.urls)),

]
