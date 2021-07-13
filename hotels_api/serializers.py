
from rest_framework import serializers

from hotels_api import models

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

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
        fields = ('name','location','guestrating','description','kinds','reviews','distance')
    def create(self,validated_data):
        print('place created')
        place = models.Place.objects.create(
            name = validated_data['name'],
            location = validated_data['location'],
            guestrating = validated_data['guestrating'],
            description  =validated_data['description'],
            reviews = validated_data['reviews'],
            kinds = validated_data['kinds'],
            distance = validated_data['distance'],

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
