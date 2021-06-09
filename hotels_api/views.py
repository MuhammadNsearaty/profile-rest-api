from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from hotels_api import models
from hotels_api import serializers

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.


class HotelViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.HotelSerializer
    permission_classes = (AllowAny,)
    queryset = models.Hotel.objects.all()
    def create(self,request):
        pass
    def retrieve(self, request, pk=None):
        # choice = request.data['choice']
        # infoDict = list(request.data['info'])
        choice = request.query_params.get('choice')
        infoDict = request.query_params.get('info')
        logger.warning(f'choice : {choice} info {infoDict}')
        # print()
        res = search_engine.get('HOTELS', choice, dict(infoDict))
        return Response({'result' : res})


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceSerializer
    permission_classes = (AllowAny,)
        # queryset = models.Place.objects.all()
    def retrieve(self, request, pk=None):
        # choice = request.data['choice']
        # infoDict = dict(request.data['info'])
        choice = request.query_params.get('choice')
        infoDict = request.query_params.get('info')
        res = search_engine.get('PLACES', choice, infoDict)
        return Response({'result' : res})
