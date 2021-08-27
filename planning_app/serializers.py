import datetime

from django.db.models import Count
from rest_framework import serializers

from planning_app import models
from profiles_app.serializers import UserProfileSerializer


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
        read_only_fields = ('type',)
        extra_kwargs = {
            'properties': {
                'required': False,
            }
        }

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.latitude = validated_data['latitude']
        instance.longitude = validated_data['longitude']
        instance.address = validated_data['address']
        instance.distance = validated_data['distance']
        instance.image = validated_data['image']
        instance.city_name = validated_data['city_name']
        instance.guest_rating = validated_data['guest_rating']
        instance.properties = validated_data['properties']
        instance.type = validated_data['type']
        instance.save()
        return instance

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


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = ('day', 'index', 'place')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        instance.place = models.Place.objects.get(id=data['place'])
        data['place'] = PlacesMicroSerializer().to_representation(instance.place)
        return data


class DaySerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(read_only=True, many=True)

    class Meta:
        model = models.Day
        fields = ('day_index', 'trip', 'activities')

    def create(self, validated_data):
        day = models.Day.objects.create(
            day_index=validated_data['day_index'], trip=validated_data['trip'])
        return day


class DayMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = ('id', 'day_index',)


# TODO implement create method for nested representation
class TripDetailsSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    days = DaySerializer(read_only=True, many=True)

    class Meta:
        model = models.Trip
        fields = ('user', 'start_date', 'days', 'trip_type')

    def create(self, validated_data):
        trip = models.Trip.objects.create(
            start_date=validated_data['start_date'], user=validated_data['user'])
        return trip

    def update(self, instance, validated_data):
        instance.start_date = validated_data['start_date']
        instance.save()
        print(f'validated data {validated_data}')
        # days_serilaizer = DaySerializer()
        # with transaction.atomic():
        #     for day in days:
        #         day_db = models.Day.get(id=day['id'])
        #         if day_db:
        #             days_serilaizer.update(day_db,day)
        #         else:
        #             models.Day.objects.create(**day)
        return instance

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
        fields = ('id', 'user', 'start_date', 'days', 'trip_type')

    def to_representation(self, instance):
        json = super().to_representation(instance)
        activities = models.Activity.objects.filter(day__in=instance.days.values('pk'))
        json['cities'] = [city_name[0] for city_name in activities.values_list('place__city_name').distinct()]
        json['image'] = f'https://loremflickr.com/320/320/places?random={instance.pk}'
        return json


class SemiAutoSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    trip1 = TripDetailsSerializer(required=True)
    trip2 = TripDetailsSerializer(required=True)

    def validate_action(self, value):
        print(f'value {value}')
        if not value:
            raise serializers.ValidationError('empty trip')
        return value
