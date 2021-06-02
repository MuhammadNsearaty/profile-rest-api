from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

from django.utils import timezone
from django.contrib.postgres.fields import ArrayField



# Create your models here.


class Location(models.Model):
    latitude = models.FloatField(null=False,default=0.0)
    longitude = models.FloatField(null=False,default=0.0)
    cityName = models.CharField(max_length=15)

class Weather(models.Model):
    temprature = models.FloatField(null=False)
    message = models.CharField(max_length=1000)
    location = models.ForeignKey(
        'Location',
        on_delete = models.CASCADE
    )
    windSpeed = models.FloatField(null=False)


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    reviewText = models.CharField(max_length=2000)
    overallRating = 0.0

class Place(models.Model):
    name = models.CharField(max_length=10)
    location = models.ForeignKey(
        'Location',
        on_delete = models.DO_NOTHING,
    )
    rank = models.FloatField(null=False,default=0.0)
    kinds = models.CharField(max_length=1000)
    description = models.CharField(max_length=100)
    reviews = ArrayField(
        models.IntegerField(),50,null=True,
    )
    # address =  models.CharField(max_length=100)

class Bookable():
    def makeAnAppointment(self):
        pass


class Room(models.Model):
    checkinDate = models.DateTimeField()
    checkoutDate  = models.DateTimeField()
    details = models.CharField(max_length=1000)

class Restaurant(Place,Bookable):
    checkinDate = models.DateTimeField()
    orderMenu = []#list(Order())
    # @override
    def makeAnAppointment():
        pass

class Hotel(Place,Bookable):
    rooms = []#list(Room())
    # @override
    def makeAnAppointment():
        pass
