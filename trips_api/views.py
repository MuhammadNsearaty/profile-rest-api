from django.db.models.query import QuerySet
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from trips_api import models
from trips_api import serializers
from trips_api import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TripSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
 
    def get_queryset(self):
        return models.Trip.objects.filter(userId=self.request.user)
