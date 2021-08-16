from rest_framework import serializers

from hotels_api import models
from profiles_api.serializers import UserProfileSerializer


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'description', 'image')

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'image': f'https://loremflickr.com/320/320/{instance.name}?random'
        }


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
