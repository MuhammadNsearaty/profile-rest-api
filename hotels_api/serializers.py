from rest_framework import serializers

from hotels_api import models
from profiles_api.serializers import UserProfileSerializer


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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = f'https://loremflickr.com/320/320/places?random={instance.pk}'
        return data


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel
        fields = ('name', 'location', 'guestrating', 'description', 'kinds', 'distance', 'address', 'imageUri')
        depth = 1

    def create(self, validated_data):
        location_object = models.Location.objects.get(id=validated_data['location'])
        hotel = models.Hotel.objects.create(
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/hotels?random={instance.pk}'
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'description')

    def create(self, validated_data):
        return models.Tag.objects.create(**validated_data)


class BlogSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = models.Blog
        fields = ('id', 'title', 'image', 'blog_text', 'date', 'tags', 'user')
        read_only_fields = ['date']

    def create(self, validated_data):
        blog = models.Blog.objects.create(
            title=validated_data['title'],
            image=validated_data['image'],
            blog_text=validated_data['blog_text'],
            user=self.context['request'].user,
        )
        return blog

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/tags?random={instance.pk}'
        return data
