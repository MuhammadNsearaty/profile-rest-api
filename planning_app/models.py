import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Property(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=1000)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=256)
    latitude = models.FloatField(null=False, default=0.0)
    longitude = models.FloatField(null=False, default=0.0)
    city_name = models.CharField(max_length=100)

    distance = models.FloatField(null=False, default=0.0)
    properties = models.ManyToManyField('Property', related_name='places')
    address = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=300,
                                   default='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque scelerisque efficitur posuere. Curabitur tincidunt placerat diam ac efficitur. Cras rutrum egestas nisl vitae pulvinar. Donec id mollis diam, id hendrerit neque.')
    # TODO make null False
    image = models.URLField(max_length=200, null=True)
    PLACE_TYPES = [
        (1, 'Place'),
        (2, 'Hotel'),
    ]
    type = models.IntegerField(choices=PLACE_TYPES, default=1)
    price = models.PositiveIntegerField(default=10)

    open_trip_map_id = models.CharField(max_length=15, default='')
    dataset_index = models.IntegerField(default=-1)

    def __str__(self):
        return self.name


class GeoNameInfo(models.Model):
    geo_name_id = models.CharField(max_length=15)
    country_name = models.CharField(max_length=100)
    wiki_link = models.URLField()
    wiki_title = models.CharField(max_length=255)
    place = models.ForeignKey(Place, related_name='geo_name_info', on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.place)} has geo name id: {self.geo_name_id}'


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
    review_text = models.CharField(max_length=700)
    RATING_CHOICES = [
        (1, 'Terrible'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent')
    ]
    overall_rating = models.IntegerField(null=False, default=1, choices=RATING_CHOICES)


class Day(models.Model):
    """Days over the trip"""
    day_index = models.PositiveIntegerField(default=0, null=False,
                                            validators=[MinValueValidator(0), MaxValueValidator(14)])
    trip = models.ForeignKey(
        'Trip',
        on_delete=models.CASCADE, related_name='days',
    )


class Activity(models.Model):
    index = models.PositiveIntegerField(null=False, default=0)
    day = models.ForeignKey(to='Day', related_name='activities', on_delete=models.CASCADE)
    place = models.ForeignKey(to='Place', related_name='activities', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"


class Trip(models.Model):
    """Places and bookings"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField(null=False)
    TYPE_CHOICES = [
        (1, 'Extended'),
        (2, 'Focused'),
    ]
    trip_type = models.IntegerField(null=False, default=1, choices=TYPE_CHOICES)
