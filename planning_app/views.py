from django.db.models import Avg, Count, CharField, Value, F
from django.db.models.functions import Concat

from rest_framework import viewsets, parsers

from shared.permissions import IsOwnerOrReadOnly
from planning_app import permissions, filters, models, serializers
from rest_framework.response import Response


class PlaceDbViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AdminOrReadOnly,)
    queryset = models.Place.objects.filter(
        type=models.Place.PLACE_TYPES[0][0]).annotate(
        guest_rating=Avg('reviews__overall_rating'), reviews_count=Count('reviews__overall_rating'))
    ordering_fields = ['name', 'distance', 'guest_rating', 'reviews_count']
    search_fields = ['name', 'address']
    filterset_class = filters.PlaceFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PlacesMiniSerializer
        return serializers.PlaceDetailsSerializer

    def perform_create(self, serializer):
        serializer.save(type=models.Place.PLACE_TYPES[0][0])


class PlacesReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = models.PlaceReview.objects.annotate(user_name=Concat(F('user__first_name'), Value(' '),
                                                                    F('user__last_name'),
                                                                    output_field=CharField()))
    filterset_class = filters.PlaceReviewFilter
    search_fields = ['review_text', 'user_name']
    ordering_fields = ('date', 'overall_rating')


class HotelDbViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AdminOrReadOnly,)
    queryset = models.Place.objects.filter(
        type=models.Place.PLACE_TYPES[1][0]).annotate(guest_rating=Avg('reviews__overall_rating'),
                                                      reviews_count=Count('reviews'))
    ordering_fields = ['name', 'distance', 'guest_rating', 'reviews_count']
    search_fields = ['name', 'address']
    filterset_class = filters.PlaceFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PlacesMiniSerializer
        return serializers.PlaceDetailsSerializer

    def perform_create(self, serializer):
        serializer.save(type=models.Place.PLACE_TYPES[1][0])


# TODO implement Create/Update methods
class TripViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = models.Trip.objects.annotate(days_count=Count('days'))
    filterset_class = filters.TripFilter
    ordering_fields = ('start_date', 'days_count')
    parser_classes = (parsers.JSONParser, )
    serializer_class = serializers.TripDetailsSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TripMiniSerializer
        return serializers.TripDetailsSerializer

    def create(self, request,*args,**kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            trip = serializer.create(request.data)
            return Response({"trip":trip})                
