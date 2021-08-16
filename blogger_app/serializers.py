from rest_framework import serializers

from profiles_app.serializers import UserProfileSerializer

from blogger_app import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'description', 'image', 'blogs')
        extra_kwargs = {'blogs': {'required': False}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = f'https://loremflickr.com/320/320/{instance.name}?random'
        return data


class BlogSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.Blog
        fields = ('id', 'title', 'image', 'blog_text', 'date', 'tags', 'user')
        read_only_fields = ['date']
        extra_kwargs = {'tags': {'required': False}}
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/tags?random={instance.pk}'
        return data
