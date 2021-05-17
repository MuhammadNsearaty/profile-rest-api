from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from profiles_api import models

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(models.UserProfile)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, models.UserProfile)
        except user.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }
#
# class ProfileFeedItemSerializer(serializers.ModelSerializer):
#     """Serializes profile fees item"""
#
#     class Meta:
#         model = models.ProfileFeedItem
#         fields = ('id', 'user_profile','status_text', 'created_on')
#         extra_kwargs = {
#             'user_profile':{
#                 'read_only':True,
#                 }
#         }

# class HelloSerializer(serializers.Serializer):
#     """Serializes a name field for testing out APIView"""
#     name = serializers.CharField(max_length=10)
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fileds = ('latitude','longitude','cityName')
    def create(self,validated_data):
        location = models.Location.objects.create_user(
        latitude = validated_data['latitude'],
        longitude = validated_data['longitude'],
        cityName = validated_data['cityName'],
        )
        return location

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel
        fields = ('name','location','ranking','description','tags','reviews','address')

    def create(self,validated_data):
        hotel = Hotel.objects.create(
            name = validated_data['name'],
            location = validated_data['location'],
            ranking = validated_data['ranking'],
            description = validated_data['description'],
            tags = validated_data['tags'],
            reviews = validated_data['reviews'],
            address = validated_data['address']
        )
        # user = Hotel.objects.create(**validated_data)
        return hotel


class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email','firstName','lastName','age','password','gender')
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
            lastName=validated_data['lastName'],
            password = validated_data['password'],
            age=validated_data['age'],
            gender=validated_data['gender']
        )
        # user = models.UserProfile.objects.create_user(**validated_data)
        return user
