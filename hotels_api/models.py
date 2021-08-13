from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.db.models.fields.related import ForeignKey

from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from trips_api import models as trip_models
# Create your models here.

class Location(models.Model):
    def Location(self,longitude,latitude):
        this.longitude = longitude
        this.latitude = latitude
    latitude = models.FloatField(null=False,default=0.0)
    longitude = models.FloatField(null=False,default=0.0)
    cityName = models.CharField(max_length=15)

class HotelReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    hotelId = models.ForeignKey(
        'Hotel',
        on_delete=models.CASCADE
    )
    reviewText = models.CharField(max_length=2000)
    overallRating = 0.0

class PlaceReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    placeId = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE
    )
    reviewText = models.CharField(max_length=2000)
    overallRating = 0.0


class Hotel(models.Model):
    name = models.CharField(max_length=10)
    location = models.ForeignKey(
        'Location',
        on_delete = models.DO_NOTHING,
    )
    distance = models.FloatField(null=False,default=0.0)
    guestrating = models.FloatField(null=False,default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    kinds = models.CharField(max_length=1000,default='')
    description = models.CharField(max_length=100,default='')
    address =  models.CharField(max_length=100,default='')
    imageUri = models.CharField(max_length=100,default='')
    


class Place(models.Model):
    name = models.CharField(max_length=10)
    location = models.ForeignKey(
        'Location',
        on_delete = models.DO_NOTHING,
    )
    distance = models.FloatField(null=False,default=0.0)
    guestrating = models.FloatField(null=False,default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    kinds = models.CharField(max_length=1000,default='')
    address =  models.CharField(max_length=100,default='')
    description = models.CharField(max_length=100,default='')
    imageUri = models.CharField(max_length=100,default='')
    


class Room(models.Model):
    hotelId = models.ForeignKey(
        'Hotel',
        on_delete=models.CASCADE
    )
    checkinDate = models.DateTimeField()
    checkoutDate  = models.DateTimeField()
    details = models.CharField(max_length=1000)

# class Restaurant(Place,Bookable):
#     checkinDate = models.DateTimeField()
#     orderMenu = []#list(Order())
#     # @override
#     def makeAnAppointment():
#         pass
