from rest_framework import serializers

from hotels_api import models as hotel_models
from hotels_api import serializers as hotel_serializers
from trips_api import models


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trip
        fields = ('userId', 'startDate')

    def create(self, validated_data):
        trip = models.Trip.objects.create(
            userId=validated_data['userId'],
            startDate=validated_data['startDate'],
        )
        return trip

    def to_representation(self, instance):
        data = super().to_representation(instance)
        days = models.Day.objects.filter(tripId=instance.pk)
        days_serializer = DaySerializer()
        json_days = [days_serializer.to_representation(day) for day in days]
        data['days'] = json_days

        return data


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = ('tripId', 'idx', 'hotels', 'places')

    def create(self, validated_data):
        day = models.Day.objects.create(
            tripId=validated_data['tripId'],
            idx=validated_data['idx'],
            hotels=validated_data['hotels'],
            places=validated_data['places'],
        )
        return day

    def to_representation(self, instance):
        data = super(DaySerializer, self).to_representation(instance)
        hotels = hotel_models.Hotel.objects.filter(id__in=instance.hotels.all())
        places = hotel_models.Place.objects.filter(id__in=instance.places.all())

        hotels_serializers = hotel_serializers.HotelSerializer()
        places_serializers = hotel_serializers.PlaceSerializer()
        json_hotels = [hotels_serializers.to_representation(hotel) for hotel in hotels.all()]
        json_places = [places_serializers.to_representation(place) for place in places.all()]
        data['hotels'] = json_hotels
        data['places'] = json_places

        return data
