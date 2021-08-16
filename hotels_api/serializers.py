from rest_framework import serializers

from hotels_api import models


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Place
        fields = ('id', 'name', 'description', 'latitude', 'longitude', 'address', 'distance', 'guest_rating', 'kinds',
                  'image', 'city_name')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = f'https://loremflickr.com/320/320/places?random={instance.pk}'
        return data


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel
        fields = ('id', 'name', 'description', 'latitude', 'longitude', 'address', 'distance', 'guest_rating', 'kinds',
                  'image', 'city_name')
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/hotels?random={instance.pk}'
        return data