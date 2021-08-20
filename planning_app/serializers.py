# from _typeshed import StrPath
import datetime

from django.db.models import Count

from rest_framework import serializers

from planning_app import models
from profiles_app.serializers import UserProfileSerializer
from profiles_app import models as profile_app_models

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Property
        fields = ('id', 'name', 'description')


class PropertyMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Property
        fields = ('id', 'name',)


class PlacesMiniSerializer(serializers.ModelSerializer):
    guest_rating = serializers.FloatField(read_only=True)
    properties = PropertyMiniSerializer(read_only=True, many=True)

    class Meta:
        model = models.Place
        fields = ('id', 'name', 'latitude', 'longitude', 'address', 'distance',
                  'image', 'city_name', 'guest_rating', 'properties', 'price', 'type')
        read_only_fields = ['type']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/hotels?random={instance.pk}'
        return data


class PlacesMicroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Place
        fields = ('id', 'name', 'address', 'distance',
                  'image', 'city_name', 'type')
        read_only_fields = ['type']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/hotels?random={instance.pk}'
        return data


class PlaceDetailsSerializer(serializers.ModelSerializer):
    guest_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = models.Place
        fields = ('id', 'name', 'description', 'latitude', 'longitude', 'address', 'distance',
                  'image', 'city_name', 'guest_rating', 'properties', 'type')
        read_only_fields = ('type', )
        extra_kwargs = {
            'properties': {
                'required': False,
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        properties_serializer = PropertySerializer(many=True, read_only=True)
        # TODO remove statement
        data['image'] = f'https://loremflickr.com/320/320/hotels?random={instance.pk}'
        queryset = models.PlaceReview.objects.filter(
            place=instance.pk).values('overall_rating').order_by().annotate(count=Count('overall_rating'))
        queryset_result = {stat['overall_rating']: stat['count'] for stat in queryset}
        data['rating_stat'] = {rate: queryset_result.get(rate, 0) for rate, _ in models.PlaceReview.RATING_CHOICES}
        data['properties'] = properties_serializer.to_representation(instance.properties)
        return data


class PlaceReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.PlaceReview
        fields = ('id', 'user', 'place', 'date', 'review_text', 'overall_rating')


# TODO implement create method for nested representation
class ActivityDetailsSerializer(serializers.ModelSerializer):
    place = PlacesMicroSerializer()

    class Meta:
        model = models.Activity
        fields = ('day', 'index', 'place')
    def create(self,validated_data):
        activity = self.create(**validated_data)
        return activity


# TODO implement create method for nested representation
class DayDetailsSerializer(serializers.ModelSerializer):
    activities = ActivityDetailsSerializer(many=True)

    class Meta:
        model = models.Day
        fields = ('id', 'day_index', 'trip','activities')
        extra_kwargs = {'activities': {'required': True}}

    def create(self,validated_data):        
        activities_data = validated_data.pop('activities')
        day = models.Trip.objects.create(
            id = validated_data['id'],
            day_index = validated_data['day_index'],
            trip = validated_data['trip']
        )
        serilaized_activities =  ActivityDetailsSerializer(data=activities_data,many=True)
        return day
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for activity in data['activities']:
            del activity['day']
        return data


class DayMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = ('id', 'day_index',)


# TODO implement create method for nested representation
class TripDetailsSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    days = DayDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = models.Trip
        fields = ('id', 'user', 'start_date', 'days')
    
    def create(self, validated_data):
        try:
            throwThis = profile_app_models.UserProfile.objects.get(validated_data['user'])
        except profile_app_models.UserProfile.DoesNotExist:
            return Response({'message':'User does not exists'})
        
        days_data = validated_data.pop('days')

        trip = models.Trip.objects.create(
            id = validated_data['id'],
            start_date = validated_data['start_date'],
        )
        serilaized_days = DayDetailsSerializer(data=days_data,read_only=True, many=True)
        
        return trip

    def validate_start_date(self, value):
        """
        Check that the start data is not in the past.
        """
        if value < datetime.date.today():
            raise serializers.ValidationError("Trip start date can't be in the past")
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['user']['birthday']
        del data['user']['gender']
        return data


class TripMiniSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.Trip
        fields = ('id', 'user', 'start_date', 'days')
