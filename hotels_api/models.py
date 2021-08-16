import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=10)
    latitude = models.FloatField(null=False, default=0.0)
    longitude = models.FloatField(null=False, default=0.0)
    city_name = models.CharField(max_length=15)

    distance = models.FloatField(null=False, default=0.0)
    guest_rating = models.FloatField(null=False, default=0.0,
                                     validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    kinds = models.CharField(max_length=1000, default='')
    description = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    # TODO make null False
    image = models.URLField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=10)
    latitude = models.FloatField(null=False, default=0.0)
    longitude = models.FloatField(null=False, default=0.0)
    city_name = models.CharField(max_length=15)
    
    distance = models.FloatField(null=False, default=0.0)
    guest_rating = models.FloatField(null=False, default=0.0,
                                     validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    kinds = models.CharField(max_length=1000, default='')
    address = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')
    # TODO make null False
    image = models.URLField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(
        'Hotel',
        on_delete=models.CASCADE
    )
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    description = models.CharField(max_length=1000)
    price = models.FloatField()
    image = models.URLField(max_length=200, null=True)


class HotelReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    hotel = models.ForeignKey(
        'Hotel',
        on_delete=models.CASCADE
    )
    review_rating = models.CharField(max_length=2000)
    overall_rating = 0.0


class PlaceReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    place = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE
    )
    review_text = models.CharField(max_length=5000)
    overall_rating = 0.0