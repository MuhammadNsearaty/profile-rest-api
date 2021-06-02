from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class FlightTicket(models.Model):
    date = models.DateTimeField()
    originCity =models.CharField(max_length=15)
    destinationCity = models.CharField(max_length=15)
    expectedDuration = models.TimeField()

class AirLine(models.Model):
    name = models.CharField(max_length=20)
    flights = []
    reviews = []#list(Review())

class Trip(models.Model):
    """Places ,ovarAllRating and bookings"""
    places = []#list(Place())
    ovarAllRating = 0.0
    bookings =[]

class Task(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    isFinished = models.BooleanField(default=True)
    category = models.CharField(max_length=10)
