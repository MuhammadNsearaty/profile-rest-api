from django.http import FileResponse

import util
import pandas as pd

from django.db import transaction
from django.db.models import Avg, Count, CharField, Value, F
from django.db.models.functions import Concat
from rest_framework import viewsets, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from planning_app.models import Place, GeoNameInfo

from search_engine.search_engine import SearchEngine

from planning_app import permissions, filters, models, serializers
from shared.permissions import IsOwnerOrReadOnly


class PlaceDbViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AdminOrReadOnly,)
    queryset = models.Place.objects.filter(
        type=models.Place.PLACE_TYPES[0][0]).annotate(
        guest_rating=Avg('reviews__overall_rating'), reviews_count=Count('reviews__overall_rating'))
    ordering_fields = ['name', 'distance', 'guest_rating', 'reviews_count']
    search_fields = ['name', 'address', 'city_name']
    filterset_class = filters.PlaceFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PlacesMiniSerializer
        return serializers.PlaceDetailsSerializer

    def perform_create(self, serializer):
        serializer.save(type=models.Place.PLACE_TYPES[0][0])


class PlacesReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = models.PlaceReview.objects.annotate(user_name=Concat(F('user__first_name'), Value(' '),
                                                                    F('user__last_name'),
                                                                    output_field=CharField()))
    filterset_class = filters.PlaceReviewFilter
    search_fields = ['review_text', 'user_name', 'place__name']
    ordering_fields = ('date', 'overall_rating')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HotelDbViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AdminOrReadOnly,)
    queryset = models.Place.objects.filter(
        type=models.Place.PLACE_TYPES[1][0]).annotate(guest_rating=Avg('reviews__overall_rating'),
                                                      reviews_count=Count('reviews'))
    ordering_fields = ['name', 'distance', 'guest_rating', 'reviews_count']
    search_fields = ['name', 'address', 'city_name']
    filterset_class = filters.PlaceFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PlacesMiniSerializer
        return serializers.PlaceDetailsSerializer

    def perform_create(self, serializer):
        serializer.save(type=models.Place.PLACE_TYPES[1][0])


# df = pd.read_csv(r"C:\Users\Nitro\Downloads\Compressed\content\cleaned_wikivector_geonames.csv")
# df = pd.read_csv(r"C:\Users\Nitro\SOURCE\profile-rest-api\assets\Hotels Recommender\SelectedFeaturesHotelDataset.csv")


class TripViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Trip.objects.annotate(days_count=Count('days'), user_name=Concat(F('user__first_name'),
                                                                                       Value(' '),
                                                                                       F('user__last_name')))
    filterset_class = filters.TripFilter
    ordering_fields = ('start_date', 'days_count')
    search_fields = ['user_name']
    parser_classes = (parsers.JSONParser,)
    serializer_class = serializers.TripDetailsSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TripMiniSerializer
        if self.action == 'plan_auto':
            return serializers.AutoPlanSerializer
        return serializers.TripDetailsSerializer

    def create(self, request, *args, **kwargs):
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
                for d_data, day in zip(days_data, days):
                    activities_data = d_data['activities']
                    for active in activities_data:
                        active['day'] = day.id
                    print(f'activity {activities_data}')
                    activities_serializer = serializers.ActivitySerializer(data=activities_data, many=True)
                    if activities_serializer.is_valid():
                        activities = activities_serializer.save()
            if serilaized_days.errors:
                print(f'serilaized_days.errors {serilaized_days.errors}')
                return Response({'message': 'invalid days data'})
            if activities_serializer.errors:
                print(f'serilaized_days.errors {activities_serializer.errors}')
                return Response({'message': 'invalid activities data'})

            return Response(serializer.to_representation(models.Trip.objects.get(id=trip.id)))

    def partial_update(self, request, *args, **kwargs):
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
                    days_serilaizer = serializers.DaySerializer(day_db, data=day, partial=True)
                    if days_serilaizer.is_valid(raise_exception=True):
                        days_serilaizer.save()
                        print(f'updated day {day_db}')
                    if days_serilaizer.errors:
                        print(f'days_serilaizer.errors {days_serilaizer.errors}')
                        return Response({'message': 'invalid days data'})

                    activities_data = day['activities']
                    for active in activities_data:
                        try:
                            active_db = models.Activity.objects.get(id=active['id'])
                            print(f'found the day {active_db}')
                            activities_serializer = serializers.ActivitySerializer(active_db, data=active, partial=True)
                            if activities_serializer.is_valid(raise_exception=True):
                                activities_serializer.save()
                                print(f'updated active {active_db}')
                            if activities_serializer.errors:
                                print(f'activities_serializer.errors {activities_serializer.errors}')
                                return Response({'message': 'invalid activities data'})

                        except models.Activity.DoesNotExist:
                            active['day'] = day_db.id
                            active.pop('id')
                            new_active_serializer = serializers.ActivitySerializer(data=active)
                            if new_active_serializer.is_valid(raise_exception=True):
                                new_active = new_active_serializer.save()
                                print(f'new activity {new_active}')
                            if new_active_serializer.errors:
                                print(f'new_active_serializer.errors {new_active_serializer.errors}')
                                return Response({'message': 'invalid activities data'})

                except models.Day.DoesNotExist:
                    day['trip'] = trip.id
                    day.pop('id')
                    new_day_serializer = serializers.DaySerializer(data=day)
                    if new_day_serializer.is_valid(raise_exception=True):
                        new_day = new_day_serializer.save()
                        print(f'created new Day {new_day}')
                    if new_day_serializer.errors:
                        print(f'new_day_serializer.errors {new_day_serializer.errors}')
                        return Response({'message': 'invalid days data'})

        return Response(serializer.data)

    @action(methods=['POST'], url_path='auto',
            detail=False,
            parser_classes=[parsers.JSONParser],
            filterset_class=None,
            ordering_fields=[],
            search_fields=[])
    def plan_auto(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            engine = SearchEngine()
            res = engine.plan_trip(serializer.validated_data)
            trip1, trip2 = util.fix_json(res)
            t1 = util.create(trip1, request.user)

            t2 = util.create(trip2, request.user)
            print(f't1 t2 result {[t1, t2]}')
            return Response({'trips': [t1.data, t2.data]})

    @action(methods=['GET'], url_path='map-view',
            detail=False,
            parser_classes=[parsers.JSONParser],
            filterset_class=None,
            ordering_fields=[],
            search_fields=[])
    def webview(self, request):
        return FileResponse(open(r'C:\Users\Nitro\SOURCE\profile-rest-api\map.html', 'rb'), as_attachment=False)

    @action(methods=['GET'], url_path='create_data', detail=False, filterset_class=None, ordering_fields=[],
            search_fields=[])
    def create_geoname_data(self, request):
        # with transaction.atomic():
        #     for index, row in df[df['country code'].isin(['SY', 'LB', 'FR', 'TR', 'IT', 'BR'])].iterrows():
        #         obj = Place.objects.create(
        #             dataset_index=index,
        #             name=str(row['name']),
        #             latitude=row['latitude'],
        #             longitude=row['longitude'],
        #             city_name=str(row['nearest city']),
        #             type=Place.PLACE_TYPES[0][0],
        #         )
        #         country_name = str(row['country'])
        #         if len(country_name) > 50:
        #             country_name = 'unknown'
        #         GeoNameInfo.objects.create(
        #             geo_name_id=row['geonameid'],
        #             country_name=country_name,
        #             wiki_title=row['wiki title'],
        #             wiki_link=row['wiki link'],
        #             place=obj,
        #         )

        # with transaction.atomic():
        #     prop_id = []
        #     for t in df.columns:
        #         if t != 'country' and t != 'name':
        #             _property, _ = models.Property.objects.get_or_create(name=t,
        #                                                                  defaults={
        #                                                                      "name": t})
        #             prop_id.append(_property.id)
        #     for index, row in df[df['country'].isin(['Lebanon', 'Syria', 'France', 'Turkey'])].iterrows():
        #         obj = models.Place.objects.create(
        #             name=row['name'], latitude=0,
        #             longitude=0, city_name='unknown',
        #             type=models.Place.PLACE_TYPES[1][0],
        #         )
        #         for t in prop_id:
        #             _property = models.Property.objects.get(id=t)
        #             if row[_property.name] != 0:
        #                 _property.places.add(obj.id)
        return Response({'message': 'Hello, World!'})
