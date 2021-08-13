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
    permission_classes = [permissions.CreateOwnTrip]
 
    def get_queryset(self):
        return models.Trip.objects.filter(userId=self.request.user)


    def create(self, request, *args, **kwargs):
        """
        verify that the POST has the request user as the obj.userId
        """
        if request.data["userId"] == str(request.user.id):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)
        else:
            return Response(status=403)
