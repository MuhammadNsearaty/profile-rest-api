from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny

from hotels_api import models
from hotels_api import serializers

import ast
import sys
sys.path.append("./Search Engine/Trips-planning-system-main/")

from search_engine.search_engine import SearchEngine


class HotelViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.HotelSerializer
    permission_classes = (AllowAny,)
    queryset = models.Hotel.objects.all()

    def list(self, request):
        choice = request.query_params.get('choice')
        infoDict = ast.literal_eval(request.query_params.get('info'))
        search_engine = SearchEngine()
        res = search_engine.get('HOTELS', choice, infoDict)
        print(f'res {type(res)}')
        # res = res[0:10]#get the first 10 hotels
        return Response({'result' : res})
    
    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)
    
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
    
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """Handle updating an object"""
    
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
    
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle removing an object"""
    
        return Response({'http_method': 'DELETE'})


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaceSerializer
    permission_classes = (AllowAny,)
    
    def list(self, request, pk=None):
        choice = request.query_params.get('choice')
        infoDict = ast.literal_eval(request.query_params.get('info'))
        search_engine = SearchEngine()
        res = search_engine.get('PLACES', choice, infoDict)
        return Response({'result' : res})

    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})


class HotelDbViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HotelSerializer
    permission_classes = (AllowAny,)
    queryset = models.Hotel.objects.all()


class PlaceDbViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HotelSerializer
    permission_classes = (AllowAny,)
    queryset = models.Place.objects.all()
    
    
        
    