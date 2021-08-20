from rest_framework import serializers

from blogger_app import models
from profiles_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object"""
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'birthday', 'gender', 'profile_picture', 'likes_count')
        ref_name = 'blogger_app_user_serializer'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profile_picture'] = f'https://loremflickr.com/320/320/users?random={instance.pk}'
        return data


class TagSerializer(serializers.ModelSerializer):
    blog_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'description', 'image', 'blog_count')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = f'https://loremflickr.com/320/320/tags?random={instance.pk}'
        # data['image'] = f'https://loremflickr.com/320/320/{instance.pk}?random={instance.pk}'
        return data


class TagMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name')


class BlogSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Blog
        fields = ('id', 'title', 'image', 'blog_text', 'date', 'tags', 'user', 'likes_count')
        read_only_fields = ['date']
        extra_kwargs = {'tags': {'required': False}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/tags?random={instance.pk}'
        data['tags'] = TagMiniSerializer(many=True).to_representation(instance.tags)
        return data


class BlogMiniSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Blog
        fields = ('id', 'title', 'image', 'date', 'user', 'likes_count')
        read_only_fields = ['date']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/tags?random={instance.pk}'
        return data


class UserLikeBlogSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    blog = BlogMiniSerializer(read_only=True)

    class Meta:
        model = models.UserLikeBlog
        fields = ('user', 'blog', 'date')
        read_only_fields = ['date']


class UserLikeSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    action = serializers.IntegerField(required=True)

    def validate_action(self, value):
        if value not in [1, 2]:
            raise serializers.ValidationError('action value must be either 1 for likes or 2 for dislikes')
        return value
