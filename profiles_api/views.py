from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated,AllowAny

from rest_framework.generics import CreateAPIView,RetrieveAPIView

from profiles_api import models
from profiles_api import serializers
from profiles_api import permissions

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})
#
# class UserProfileFeedViewSet(viewsets.ModelViewSet):
#     """Handles creating, reading and updating profile feed items"""
#     authentication_classes = (TokenAuthentication,)
#     serializer_class = serializers.ProfileFeedItemSerializer
#     queryset = models.ProfileFeedItem.objects.all()
#     permission_classes = (
#         permissions.UpdateOwnStatus,
#         IsAuthenticated,
#     )
#     def perform_create(self, serializer):
#         """Sets the user profile to the logged in user"""
#         serializer.save(user_profile=self.request.user)
# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)

class UserLogInApiView(ObtainAuthToken):
    """Handle creating user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HotelSerializer
    queryset = models.Hotel.objects.all()

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    # queryset = models.UserProfile.objects.all()

    # authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('firstName','email')
    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     status_code = status.HTTP_201_CREATED
    #     response = {
    #         'success' : 'True',
    #         'status code' : status_code,
    #         'message': 'User registered  successfully',
    #         }

        # return Response(response, status=status_code)
    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        return Response(response, status=status_code)


    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})
