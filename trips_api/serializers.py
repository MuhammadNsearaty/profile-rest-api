from django.db.models.query import QuerySet
from rest_framework import serializers

from trips_api import models

class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Trip
        fields = ('userId','startDate')
    def create(self,validated_data):
        trip = models.Trip.objects.create(
        userId = validated_data['userId'],
        startDate = validated_data['startDate'],
        )
        return trip

    def to_representation(self, instance):
        data = super(TripSerializer, self).to_representation(instance)
        days = models.Day.objects.filter(tripId=instance.pk)
        days_serializer = DaySerializer()
        json_days = [days_serializer.to_representation(day) for day in days]
        data['days'] = json_days
        return data

class DaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Day
        fields = ('tripId','idx')
    def create(self,validated_data):
        day = models.Day.objects.create(
        tripId = validated_data['tripId'],
        idx = validated_data['idx'],
        )
        return day