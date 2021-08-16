from django_filters import filters, filterset
from trips_api import models


class TripFilter(filterset.FilterSet):
    start_date = filters.DateFromToRangeFilter()

    class Meta:
        model = models.Trip
        fields = ['start_date', 'user']
