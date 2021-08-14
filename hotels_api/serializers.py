from rest_framework import serializers

from hotels_api import models


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('latitude', 'longitude', 'cityName')

    def create(self, validated_data):
        location = models.Location.objects.create(
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            cityName=validated_data['cityName'],
        )
        return location


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Place
        fields = ('name', 'location', 'guestrating', 'description', 'kinds', 'distance', 'address', 'imageUri')
        depth = 1

    def create(self, validated_data):
        location_object = models.Location.objects.get(id=validated_data['location'])
        place = models.Place.objects.create(
            name=validated_data['name'],
            location=location_object,
            guestrating=validated_data['guestrating'],
            description=validated_data['description'],
            kinds=validated_data['kinds'],
            distance=validated_data['distance'],
            address=validated_data['address'],
            imageUri=validated_data['imageUri'],
        )
        return place
    # throw this function at end
    def to_representation(self, instance):
        instance.imageUri = f'https://loremflickr.com/320/320/places?random={instance.pk}'
        instance.save()
        data = super().to_representation(instance)
        return data


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel
        fields = ('name', 'location', 'guestrating', 'description', 'kinds', 'distance', 'address', 'imageUri')
        depth = 1

    def create(self, validated_data):
        location_object = models.Location.objects.get(id=validated_data['location'])
        hotel = models.Place.objects.create(
            name=validated_data['name'],
            location=location_object,
            guestrating=validated_data['guestrating'],
            description=validated_data['description'],
            kinds=validated_data['kinds'],
            distance=validated_data['distance'],
            address=validated_data['address'],
            imageUri=validated_data['imageUri'],
        )

        return hotel

    # throw this function at end
    def to_representation(self, instance):
        instance.imageUri = f'https://loremflickr.com/320/320/hotels?random={instance.pk}'
        instance.save()
        data = super().to_representation(instance)
        return data
