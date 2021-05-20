from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from enum import Enum
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
# from profiles_api import serializers

# Tags = Enum('','','')
# RatingPOV = Enum('','','')


class Location(models.Model):
    latitude = models.FloatField(null=False,default=0.0)
    longitude = models.FloatField(null=False,default=0.0)
    cityName = models.CharField(max_length=15)

class Weather(models.Model):
    temprature = models.FloatField(null=False)
    message = models.CharField(max_length=1000)
    # condition =
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
    reviewText = models.CharField(max_length=1000)
    overallRating = 0.0

class Place(models.Model):
    name = models.CharField(max_length=10)
    location = models.ForeignKey(
        'Location',
        on_delete = models.DO_NOTHING,
    )
    ranking = models.FloatField(null=False,default=0.0)
    description = models.CharField(max_length=100)

    # reviews  = serializers.ListField(child = serializers.IntegerField())

    tags = []#list(Tags)
    #reviews = []#list(Review())
    reviews = ArrayField(
        models.IntegerField(),50,null=True,
    )
    address =  models.CharField(max_length=100)

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

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255,default='')
    lastName = models.CharField(max_length=255,default='')
    tripsHistory = []#list(Trip())
    tasks = []#list(Task())
    currentTrip = Trip()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email
#
# class ProfileFeedItem(models.Model):
#     """Profile status update"""
#     user_profile = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     status_text = models.CharField(max_length=255)
#     created_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         """Return the model as a string"""
#         return self.status_text
