from django.db.models import Avg, Count, CharField, Value, F
from django.db.models.functions import Concat

from rest_framework import viewsets, parsers

from shared.permissions import IsOwnerOrReadOnly
from planning_app import permissions, filters, models, serializers
from rest_framework.response import Response
from django.db import transaction


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
    search_fields = ['review_text', 'user_name', 'place__name']
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
    queryset = models.Trip.objects.annotate(days_count=Count('days'), user_name=Concat(F('user__first_name'),
                                                                                       Value(' '), F('user__last_name')
                                                                                       ))
    filterset_class = filters.TripFilter
    ordering_fields = ('start_date', 'days_count')
    search_fields = ['user_name']
    parser_classes = (parsers.JSONParser, )
    serializer_class = serializers.TripDetailsSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TripMiniSerializer
        return serializers.TripDetailsSerializer

    def create(self, request,*args,**kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.validated_data
            valid_data['user'] = request.user
            trip = serializer.create(valid_data)
            days_data = request.data.pop('days')
            for day in days_data:
                day["trip"] = trip.id
            serilaized_days = serializers.DaySerializer(data=days_data, many=True)
            if serilaized_days.is_valid():
                days = serilaized_days.save()
                for d_data,day in zip(days_data,days):
                    activities_data = d_data['activities']
                    for active in activities_data:
                        active['day'] = day.id
                    print(f'activity {activities_data}')
                    activities_serializer = serializers.ActivitySerializer(data=activities_data,many=True)
                    if activities_serializer.is_valid():
                        activities = activities_serializer.save()
            if serilaized_days.errors:
                 print(f'serilaized_days.errors {serilaized_days.errors}')
                 return Response({'message':'invalid days data'})
            if activities_serializer.errors:
                print(f'serilaized_days.errors {activities_serializer.errors}')
                return Response({'message':'invalid activities data'})

            return Response(serializer.to_representation(models.Trip.objects.get(id=trip.id)))

    def patch(self, request, *args, **kwargs):
        # update the trip
        trip = models.Trip.objects.get(id=request.data['id'])
        serializer = self.serializer_class(trip, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # update the days
        days = request.data['days']
        
        with transaction.atomic():
            for day in days:
                try:
                    day_db = models.Day.objects.get(id=day['id'])
                    print(f'found the day {day_db}')
                    days_serilaizer = serializers.DaySerializer(day_db,data=day,partial=True)
                    if days_serilaizer.is_valid(raise_exception=True):
                        days_serilaizer.save()
                        print(f'updated day {day_db}')
                    if days_serilaizer.errors:
                        print(f'days_serilaizer.errors {days_serilaizer.errors}')
                        return Response({'message':'invalid days data'})

                    activities_data = day['activities']
                    for active in activities_data:
                        try:
                            active_db = models.Activity.objects.get(id=active['id'])
                            print(f'found the day {active_db}')
                            activities_serializer = serializers.ActivitySerializer(active_db,data=active,partial=True)
                            if activities_serializer.is_valid(raise_exception=True):
                                activities_serializer.save()
                                print(f'updated active {active_db}')
                            if activities_serializer.errors:
                                print(f'activities_serializer.errors {activities_serializer.errors}')
                                return Response({'message':'invalid activities data'})
                            
                        except models.Activity.DoesNotExist:
                            active['day'] = day_db.id
                            active.pop('id')
                            new_active_serializer = serializers.ActivitySerializer(data=active)
                            if new_active_serializer.is_valid(raise_exception=True):
                                new_active = new_active_serializer.save()
                                print(f'new activity {new_active}')
                            if new_active_serializer.errors:
                                print(f'new_active_serializer.errors {new_active_serializer.errors}')
                                return Response({'message':'invalid activities data'})
                    
                except models.Day.DoesNotExist:
                    day['trip'] = trip.id
                    day.pop('id')
                    new_day_serializer = serializers.DaySerializer(data=day)
                    if new_day_serializer.is_valid(raise_exception=True):
                        new_day = new_day_serializer.save()
                        print(f'created new Day {new_day}')
                    if new_day_serializer.errors:
                        print(f'new_day_serializer.errors {new_day_serializer.errors}')
                        return Response({'message':'invalid days data'})

        

        return Response(serializer.data)
