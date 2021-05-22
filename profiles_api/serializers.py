from rest_framework import serializers
from profiles_api import models
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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fileds = ('latitude','longitude','cityName')
    def create(self,validated_data):
        location = models.Location.objects.create(
        latitude = validated_data['latitude'],
        longitude = validated_data['longitude'],
        cityName = validated_data['cityName'],
        )
        return location


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Place
        fields = ('name','location','rank','description','kinds','reviews')
    def create(self,validated_data):
        place = models.Place.objects.create(
            name = validated_data['name'],
            location = validated_data['location'],
            rank = validated_data['rank'],
            description  =validated_data['description'],
            reviews = validated_data['reviews'],
            kinds = validated_data['kinds']
        )
        return place

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel
        fields = ('name','location','rank','description','kinds','reviews')

    def create(self,validated_data):
        hotel = Hotel.objects.create(
            name = validated_data['name'],
            location = validated_data['location'],
            rank = validated_data['rank'],
            description = validated_data['description'],
            kinds = validated_data['kinds'],
            reviews = validated_data['reviews'],
        )
        # user = Hotel.objects.create(**validated_data)
        return hotel


class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email','firstName','password')
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
            password = validated_data['password']
        )

        return user
