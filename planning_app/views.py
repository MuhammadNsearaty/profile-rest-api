from django.db.models import Avg

from rest_framework import viewsets

from shared.permissions import IsOwnerOrReadOnly
from planning_app import permissions, filters, models, serializers


class PlaceDbViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    queryset = models.Place.objects.filter(
        type=models.PLACE_TYPES[0][0]).annotate(guest_rating=Avg('reviews__overall_rating'))
    ordering_fields = ['name', 'distance', 'guest_rating']
    search_fields = ['name', 'address']

    def perform_create(self, serializer):
        serializer.save(type=models.PLACE_TYPES[1][0])


class PlacesReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = models.PlaceReview.objects.all()
    filterset_class = filters.PlaceReviewFilter
    search_fields = ['review_text']
    ordering_fields = ('date', 'overall_rating')


class HotelDbViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    queryset = models.Place.objects.filter(
        type=models.PLACE_TYPES[1][0]).annotate(guest_rating=Avg('reviews__overall_rating'))
    ordering_fields = ['name', 'distance', 'guest_rating']
    search_fields = ['name', 'address']

    def perform_create(self, serializer):
        serializer.save(type=models.PLACE_TYPES[0][0])


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TripSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Trip.objects.all()
    filterset_class = filters.TripFilter
    ordering_fields = ('start_date', )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

