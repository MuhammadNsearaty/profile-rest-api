from typing import Dict

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from rest_framework import viewsets, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from profiles_app import filters
from profiles_app import models
from profiles_app import permissions
from profiles_app import serializers


class UserRegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Handle creating users"""

    serializer_class = serializers.UserProfileSerializer
    permission_classes = (AllowAny,)
    user_serializer = serializers.UserProfileSerializer(read_only=True)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            token = Token.objects.create(user=user)
            return Response({
                'token': token.key,
                'user': self.user_serializer.to_representation(user),
            })


class UserLoginApiView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Handle getting authentication token and users login"""
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        token, created = serializer.get_or_create(validated_data=serializer.validated_data)
        user = serializer.validated_data['user']
        headers = self.get_success_headers({'token': token, 'user': user})
        return Response(serializer.to_representation({'token': token, 'user': user}),
                        status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED, headers=headers)


class UserProfilesApiView(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.annotate(name=Concat('first_name', Value(' '), 'last_name',
                                                               output_field=CharField())).all()
    ordering_fields = ('name', 'birthday',)
    search_fields = ('name', 'email',)
    filterset_class = filters.UserProfileFilter
    permission_classes = (permissions.OwnerOrAdminOnly,)

    @action(detail=False, url_path='logout', methods=['GET'], permission_classes=(IsAuthenticated,))
    def logout(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)


class DevicesViewSet(viewsets.ModelViewSet):
    """handles CRUD operations on users devices"""

    serializer_class = serializers.DeviceInfoSerializer
    permission_classes = (permissions.DeviceOwnerOrAdminOnly,)
    ordering_fields = ['app_version', 'build_number']
    filterset_fields = ['user', 'os', 'os_version']
    search_fields = ['model', 'brand']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @staticmethod
    def validate_own(data: Dict):
        uuid = data.get('uuid', None)
        if not uuid:
            return False
        return True

    @action(detail=False, url_path='update', methods=['PUT'])
    def update_own(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if self.validate_own(request.data):
            try:
                obj = models.DeviceInfo.objects.get(uuid=request.data['uuid'])
                serializer = serializers.DeviceInfoSerializer(obj, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                obj = serializer.update(obj, serializer.validated_data)
                return Response(serializer.to_representation(obj))
            except ObjectDoesNotExist:
                if serializer.is_valid(raise_exception=True):
                    validated_data = serializer.validated_data
                    validated_data['user'] = request.user
                    obj = serializer.create(validated_data)
                    return Response(serializer.to_representation(obj))
        serializer.is_valid(raise_exception=True)

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.DeviceInfo.objects.all()
        return models.DeviceInfo.objects.filter(user=self.request.user)
