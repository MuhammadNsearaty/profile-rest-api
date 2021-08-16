from django.db.models import Avg
from django.db.models import F

from rest_framework import serializers

from planning_app import models
from profiles_app.serializers import UserProfileSerializer


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Property
        fields = ('id', 'name', 'description')


class PlaceSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    guest_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = models.Place
        fields = ('id', 'name', 'description', 'latitude', 'longitude', 'address', 'distance',
                  'properties',
                  'image', 'city_name', 'guest_rating')
        extra_kwargs = {'properties': {'required': False}}
        read_only_fields = ['type']
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/hotels?random={instance.pk}'
        return data


class PlaceReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.PlaceReview
        fields = ('id', 'user', 'place', 'date', 'review_text', 'overall_rating')


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = ('id', 'trip', 'day_index', 'places')
        extra_kwargs = {'places': {'required': False}}


class TripSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.Trip
        fields = ('id', 'user', 'start_date', 'days')
        extra_kwargs = {'days': {'required': False}}
        depth = 2

    def to_representation(self, instance):

        return super().to_representation(instance)

