from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from profiles_api import models

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


# class UserLoginSerializer(serializers.Serializer):
#
#     email = serializers.CharField(max_length=255)
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     def validate(self, data):
#         email = data.get("email", None)
#         password = data.get("password", None)
#         user = authenticate(email=email, password=password)
#         if user is None:
#             raise serializers.ValidationError(
#                 'A user with this email and password is not found.'
#             )
#         try:
#             payload = JWT_PAYLOAD_HANDLER(models.UserProfile)
#             jwt_token = JWT_ENCODE_HANDLER(payload)
#             update_last_login(None, models.UserProfile)
#         except user.DoesNotExist:
#             raise serializers.ValidationError(
#                 'User with given email and password does not exists'
#             )
#         return {
#             'email':user.email,
#             'token': jwt_token
#         }
#


class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email','firstName','lastName','password')
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
                }
        }
    def create(self, validated_data):
        """Create and return a new user"""
        user  = models.UserProfile.objects.create(
            email=validated_data['email'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            password = validated_data['password']
        )
        # user = models.UserProfile.objects.create_user(**validated_data)
        return user
