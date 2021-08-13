from django.db import models
from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator
from hotels_api import models as hotel_models


class Day(models.Model):
    """Days over the trip"""
    idx = models.IntegerField(default=0, null=False, validators=[MinValueValidator(1), MaxValueValidator(15)])
    hotels = models.ManyToManyField(hotel_models.Hotel)
    places = models.ManyToManyField(hotel_models.Place)
    tripId =  models.ForeignKey(
        'Trip',
        on_delete=models.CASCADE,
    )


class Trip(models.Model):
    """Places ,ovarAllRating and bookings"""
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    startDate = models.DateField(null=False)
