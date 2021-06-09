from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from profiles_api import models

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


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
        user  = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            password = validated_data['password']
        )
        # user = models.UserProfile.objects.create_user(**validated_data)
        return user
