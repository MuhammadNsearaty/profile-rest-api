from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication



from hotels_api import models
from hotels_api import serializers

# Create your views here.


class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HotelSerializer
    # queryset = models.Hotel.objects.all()
    def retrieve(self, request, pk=None):
        choice = request.data['choice']
        infoDict = dict(request.data['info'])
        res = search_engine.get('HOTELS', choice, infoDict)
        return Response({'result' : res})


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceSerializer

        # queryset = models.Place.objects.all()
    def retrieve(self, request, pk=None):
        choice = request.data['choice']
        infoDict = dict(request.data['info'])
        res = search_engine.get('PLACES', choice, infoDict)
        return Response({'result' : res})
