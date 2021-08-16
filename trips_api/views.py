from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from trips_api import models
from trips_api import permissions
from trips_api import serializers
from trips_api import filters


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TripSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.CreateOwnTrip]
    filterset_class = filters.TripFilter
    ordering_fields = ('start_date', )

    def get_queryset(self):
        return models.Trip.objects.all()

    def create(self, request, *args, **kwargs):
        """
        verify that the POST has the request user as the obj.user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
