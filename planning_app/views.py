from rest_framework import viewsets

from shared.permissions import IsOwnerOrReadOnly
from planning_app import permissions, filters, models, serializers


class PlaceDbViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    queryset = models.Place.objects.filter(type=models.PLACE_TYPES[0][0])
    ordering_fields = ['name', 'distance']
    search_fields = ['name', 'address']

    def perform_create(self, serializer):
        serializer.save(type=models.PLACE_TYPES[1][0])


class PlacesReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly, )
    ordering_fields = ('date', 'overall_rating')
    filterset_class = filters.PlaceReviewFilter
    queryset = models.PlaceReview.objects.all()
    search_fields = ['review_text']
    serializer_class = serializers.PlaceReviewSerializer


class HotelDbViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    queryset = models.Place.objects.filter(type=models.PLACE_TYPES[1][0])
    ordering_fields = ['name', 'distance']
    search_fields = ['name', 'address']

    def perform_create(self, serializer):
        serializer.save(type=models.PLACE_TYPES[0][0])


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TripSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = filters.TripFilter
    ordering_fields = ('start_date', )
    queryset = models.Trip.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

