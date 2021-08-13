from typing import Dict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from profiles_api import models
from profiles_api import permissions
from profiles_api import serializers


class HelloView(APIView):

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserLoginApiView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Handle getting authentication token and users login"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = serializers.AuthTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': serializers.UserProfileSerializer().to_representation(user),
        })


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Handle creating users"""

    serializer_class = serializers.UserProfileSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

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


def validate_own(data: Dict):
    uuid = data.get('uuid', None)
    if not uuid:
        return False
    return True


class DevicesViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.DeviceInfoSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = models.DeviceInfo.objects.all()
    permission_classes = (IsAuthenticated, permissions.UpdateOwnDevice)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, url_path='update', methods=['PUT'])
    def update_own(self, request: Request, pk=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        if validate_own(request.data):
            try:
                obj = models.DeviceInfo.objects.get(uuid=request.data['uuid'])
                del request.data['uuid']
                if serializer.is_valid():
                    obj = serializer.update(obj, serializer.validated_data)
                    return Response(serializer.to_representation(obj))
            except ObjectDoesNotExist:
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    validated_data['user'] = request.user
                    obj = serializer.create(validated_data)
                    return Response(serializer.to_representation(obj))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
