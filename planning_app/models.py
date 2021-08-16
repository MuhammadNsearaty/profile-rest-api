import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Property(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name


PLACE_TYPES = [
    (1, 'Place'),
    (2, 'Hotel'),
]


class Place(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(null=False, default=0.0)
    longitude = models.FloatField(null=False, default=0.0)
    city_name = models.CharField(max_length=15)
    
    distance = models.FloatField(null=False, default=0.0)
    properties = models.ManyToManyField('Property', related_name='places')
    address = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')
    # TODO make null False
    image = models.URLField(max_length=200, null=True)

    type = models.IntegerField(choices=PLACE_TYPES, default=1)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE
    )
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    description = models.CharField(max_length=1000)
    price = models.FloatField()
    image = models.URLField(max_length=200, null=True)


class PlaceReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='reviews',
    )
    place = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE, related_name='reviews',
    )
    date = models.DateField(default=datetime.date.today)
    review_text = models.CharField(max_length=5000)
    overall_rating = models.IntegerField(null=False, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])


class Day(models.Model):
    """Days over the trip"""
    day_index = models.IntegerField(default=0, null=False, validators=[MinValueValidator(1), MaxValueValidator(15)])
    places = models.ManyToManyField(Place, related_name="days")
    trip = models.ForeignKey(
        'Trip',
        on_delete=models.CASCADE, related_name='days',
    )


class Trip(models.Model):
    """Places ,overallRating and bookings"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField(null=False)
