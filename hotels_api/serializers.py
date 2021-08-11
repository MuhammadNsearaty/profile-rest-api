
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
        fields = ('name','location','guestrating','description','kinds','distance','address','imageUri')
    def create(self,validated_data):
        place = models.Place.objects.create(
            name = validated_data['name'],
            location = validated_data['location'],
            guestrating = validated_data['guestrating'],
            description  =validated_data['description'],
            kinds = validated_data['kinds'],
            distance = validated_data['distance'],
            address = validated_data['address'],
            imageUri = validated_data['imageUri'],
        )
        return place

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel
        fields = ('name','location','guestrating','description','kinds','distance','address','imageUri')
    def create(self,validated_data):
        hotel = models.Place.objects.create(
            name = validated_data['name'],
            location = validated_data['location'],
            guestrating = validated_data['guestrating'],
            description  =validated_data['description'],
            kinds = validated_data['kinds'],
            distance = validated_data['distance'],
            address = validated_data['address'],
            imageUri = validated_data['imageUri'],
        )
        return hotel
