from django_filters import filters, filterset
from planning_app import models


class TripFilter(filterset.FilterSet):
    start_date = filters.DateFromToRangeFilter()

    class Meta:
        model = models.Trip
        fields = ['start_date', 'user']


class PlaceReviewFilter(filterset.FilterSet):
    date = filters.DateFromToRangeFilter()
    overall_rating = filters.RangeFilter()

    class Meta:
        model = models.PlaceReview
        fields = ['date', 'user', 'place', 'overall_rating']

