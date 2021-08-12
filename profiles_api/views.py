from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

from rest_framework.permissions import IsAuthenticated,AllowAny

from rest_framework.generics import CreateAPIView,RetrieveAPIView
import django
from profiles_api import models
from profiles_api import serializers
from profiles_api import permissions
from rest_framework.decorators import action


from django.http import HttpResponse, JsonResponse

class HelloView(APIView):

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserLogInApiView(ObtainAuthToken):
    """Handle creating user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # # serializer_class = serializers.LoginSerializer
    #
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': serializers.UserProfileSerializer().to_representation(user),
        })


class UserRegisterViewSet(APIView):
    """Handle creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    # queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    
    # def post(self, request):
    #     """Create a new hello message."""
    #     serializer = self.serializer_class(data=request.data)
        
    #     if serializer.is_valid():
    #         name = serializer.validated_data.get('name')
    #         message = f'Hello {name}!'
    #         return Response({'message': message})
    #     else:
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.create(request.data)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': serializers.UserProfileSerializer().to_representation(user),
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
