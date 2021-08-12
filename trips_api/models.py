from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class Day(models.Model):
    """Days over the trip"""
    idx = models.IntegerField(default=0,null=False,validators=[MinValueValidator(1), MaxValueValidator(15)])
    tripId =  models.ForeignKey(
        'Trip',
        on_delete=models.CASCADE
    )

class Trip(models.Model):
    """Places ,ovarAllRating and bookings"""
    userId =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    startDate = models.DateField(null=False)
