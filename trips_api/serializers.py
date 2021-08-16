from rest_framework import serializers

from hotels_api import serializers as hotel_serializers
from trips_api import models
from profiles_api.serializers import UserProfileSerializer


class DaySerializer(serializers.ModelSerializer):
    hotels = hotel_serializers.HotelSerializer(many=True)
    places = hotel_serializers.PlaceSerializer(many=True)

    class Meta:
        model = models.Day
        fields = ('id', 'trip', 'day_index', 'hotels', 'places')

    # def create(self, validated_data):
    #     day = models.Day.objects.create(
    #         trip=validated_data['trip'],
    #         idx=validated_data['idx'],
    #         hotels=validated_data['hotels'],
    #         places=validated_data['places'],
    #     )
    #     return day

    # def to_representation(self, instance):
    #     data = super(DaySerializer, self).to_representation(instance)
    #
    #     hotels_serializers = hotel_serializers.HotelSerializer(many=True)
    #     places_serializers = hotel_serializers.PlaceSerializer(many=True)
    #     json_hotels = [hotels_serializers.to_representation(hotel) for hotel in data['hotels']]
    #     json_places = [places_serializers.to_representation(place) for place in data['places']]
    #     data['hotels'] = json_hotels
    #     data['places'] = json_places
    #
    #     return data


class TripSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    days = DaySerializer(read_only=True, many=True)

    class Meta:
        model = models.Trip
        fields = ('id', 'user', 'start_date', 'days')

    def create(self, validated_data):
        trip = models.Trip.objects.create(
            user=self.context['request'].user,
            start_date=validated_data['start_date'],
        )
        return trip

    def to_representation(self, instance):
        data = super().to_representation(instance)
        days = models.Day.objects.filter(trip=instance.pk)
        data['days'] = self.get_fields()['days'].to_representation(days)
        return data
