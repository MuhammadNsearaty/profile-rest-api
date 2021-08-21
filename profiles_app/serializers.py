import datetime

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from profiles_app import models


class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'birthday', 'gender', 'password', 'profile_picture',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def validate_birthday(self, value):
        """
        Check that the birthday is not in future.
        """
        if value > datetime.date.today():
            raise serializers.ValidationError("The date of birth is not valid")
        return value

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_picture=validated_data.get('profile_picture', None),
            birthday=validated_data['birthday'],
            gender=validated_data['gender'],
            password=validated_data['password'],
        )
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profile_picture'] = f'https://loremflickr.com/320/320/users?random={instance.pk}'
        return data


class DeviceInfoSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.DeviceInfo
        fields = ('uuid', 'app_name', 'app_version', 'build_number', 'fcm_token', 'os_version', 'os', 'brand', 'model',
                  'user', 'id')


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    user = UserProfileSerializer(read_only=True)

    token = serializers.CharField(read_only=True)

    class Meta:
        model = Token
        fields = ('email', 'password', 'user', 'token')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        return {'user': user}

    def get_or_create(self, validated_data):
        return Token.objects.get_or_create(user=validated_data['user'])

    def to_representation(self, instance):
        user_repr = self.get_fields()['user'].to_representation(instance['user'])
        user_repr['profile_picture'] = f'https://loremflickr.com/320/320/person?random={instance["user"].pk}'
        return {
            'token': instance['token'].key,
            'user': user_repr,
        }
