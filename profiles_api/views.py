from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import models
from profiles_api import serializers
from profiles_api import permissions

class HelloView(APIView):

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class UserLogInApiView(ObtainAuthToken):
    """Handle creating user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HotelSerializer
    # queryset = models.Hotel.objects.all()
    def retrieve(self, request, pk=None):
        choice = request.data['choice']
        infoDict = dict(request.data['info'])
        res = search_engine.get('HOTELS', choice, infoDict)
        return Response({'result' : res})


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceSerializer

        # queryset = models.Place.objects.all()
    def retrieve(self, request, pk=None):
        choice = request.data['choice']
        infoDict = dict(request.data['info'])
        res = search_engine.get('PLACES', choice, infoDict)
        return Response({'result' : res})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer

    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('firstName','email')
