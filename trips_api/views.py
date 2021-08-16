from rest_framework import viewsets

from trips_api import models
from trips_api import permissions
from trips_api import serializers
from trips_api import filters


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TripSerializer
    permission_classes = [permissions.CreateOwnTrip]
    filterset_class = filters.TripFilter
    ordering_fields = ('start_date', )
    queryset = models.Trip.objects.all()
