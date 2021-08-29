import datetime

from django.db import transaction
from rest_framework.response import Response

from planning_app import models as planning_models
from planning_app import serializers as planning_serializers


def fix_json(data):
    new_trip1 = {"start_date": datetime.date.today().isoformat()}
    tmp_days = []
    with transaction.atomic():
        for day in data["trip1"]["days"]:
            activity_index = 1
            tmp_day = {
                "day_index": day["day_index"],
            }
            tmp_activities = []
            for activity in day["items"]:
                tmp_active = {"index": activity_index}
                place, created = planning_models.Place.objects.get_or_create(
                    open_trip_map_id=activity["item_id"],
                    defaults={'name': activity['name'], "latitude": activity["coordinate"]["lat"],
                              "longitude": activity["coordinate"]["lon"], "city_name": activity["city"],
                              "open_trip_map_id": activity["item_id"], "type": activity['type']
                              })
                tmp_active["place"] = place.id
                types = activity["item_type"]
                for t in types:
                    if t:
                        _property, created_property = planning_models.Property.objects.get_or_create(name=t,
                                                                                                     defaults={"name": t})
                        if not created_property:
                            _property.places.add(place.id)

                activity_index += 1
                tmp_activities.append(tmp_active)
            tmp_day["activities"] = tmp_activities
            tmp_days.append(tmp_day)
        new_trip1["days"] = tmp_days

    new_trip2 = {"start_date": datetime.date.today().isoformat()}
    tmp_days = []
    with transaction.atomic():
        for day in data["trip2"]["days"]:
            activity_index = 1
            tmp_day = {
                "day_index": day["day_index"],
            }
            tmp_activities = []
            for activity in day["items"]:
                tmp_active = {"index": activity_index}

                place, created = planning_models.Place.objects.get_or_create(
                    open_trip_map_id=activity["item_id"],
                    defaults={'name': activity['name'], "latitude": activity["coordinate"]["lat"],
                              "longitude": activity["coordinate"]["lon"], "city_name": activity["city"],
                              "open_trip_map_id": activity["item_id"]
                              })
                tmp_active["place"] = place.id
                types = activity["item_type"]
                for t in types:
                    if t:
                        _property, created_property = planning_models.Property.objects.get_or_create(name=t,
                                                                                                     defaults={"name": t})
                        if not created_property:
                            _property.places.add(place.id)
                activity_index += 1
                tmp_activities.append(tmp_active)
            tmp_day["activities"] = tmp_activities
            tmp_days.append(tmp_day)
        new_trip2["days"] = tmp_days

    return new_trip1, new_trip2


def create(data, user):
    serializer = planning_serializers.TripDetailsSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        valid_data = serializer.validated_data
        valid_data['user'] = user
        trip = serializer.create(valid_data)
        days_data = data.pop('days')
        for day in days_data:
            day["trip"] = trip.id
        serilaized_days = planning_serializers.DaySerializer(data=days_data, many=True)
        if serilaized_days.is_valid():
            days = serilaized_days.save()
            for d_data, day in zip(days_data, days):
                activities_data = d_data['activities']
                for active in activities_data:
                    active['day'] = day.id
                print(f'activity {activities_data}')
                activities_serializer = planning_serializers.ActivitySerializer(data=activities_data, many=True)
                if activities_serializer.is_valid():
                    activities = activities_serializer.save()
        if serilaized_days.errors:
            print(f'serilaized_days.errors {serilaized_days.errors}')
            return Response({'message': 'invalid days data'})
        if activities_serializer.errors:
            print(f'serilaized_days.errors {activities_serializer.errors}')
            return Response({'message': 'invalid activities data'})

        return Response(serializer.to_representation(planning_models.Trip.objects.get(id=trip.id)))
