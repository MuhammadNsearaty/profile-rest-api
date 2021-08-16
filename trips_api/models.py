from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from hotels_api import models as hotel_models


class Day(models.Model):
    """Days over the trip"""
    day_index = models.IntegerField(default=0, null=False, validators=[MinValueValidator(1), MaxValueValidator(15)])
    hotels = models.ManyToManyField(hotel_models.Hotel)
    places = models.ManyToManyField(hotel_models.Place)
    trip = models.ForeignKey(
        'Trip',
        on_delete=models.CASCADE,
    )


class Trip(models.Model):
    """Places ,overallRating and bookings"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField(null=False)
