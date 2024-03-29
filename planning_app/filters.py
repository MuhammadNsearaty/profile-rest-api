from functools import reduce

from django import forms
from django.core.exceptions import ValidationError
from django_filters import filters, filterset

from planning_app import models


class TripFilter(filterset.FilterSet):
    start_date = filters.DateFromToRangeFilter()
    days_count = filters.RangeFilter(label="Days Count")

    class Meta:
        model = models.Trip
        fields = ['user']


class PlaceReviewFilter(filterset.FilterSet):
    date = filters.DateFromToRangeFilter()
    overall_rating = filters.RangeFilter()

    class Meta:
        model = models.PlaceReview
        fields = ['date', 'user', 'place', 'overall_rating']


class PlaceFilterForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        properties = cleaned_data.get("properties")
        if properties:
            for value in properties:
                try:
                    int(value)
                except ValueError:
                    raise ValidationError({'properties': 'all values must be integers'})
        return cleaned_data


class PlaceFilter(filterset.FilterSet):
    properties = filters.BaseCSVFilter(
        field_name='properties',
        method='filter_properties',
    )
    guest_rating = filters.RangeFilter(label='Guest Ratings')
    reviews_count = filters.RangeFilter(label='Total Reviews Count')
    distance = filters.RangeFilter(label='Distance to City Center')

    def filter_properties(self, queryset, name, value):
        if self.is_valid():
            if value:
                return reduce(lambda x, y: x & y, [queryset.filter(properties=prop) for prop in value])
            return queryset

    class Meta:
        model = models.Place
        form = PlaceFilterForm
        fields = {
            'city_name': ['contains', 'exact'],
        }
