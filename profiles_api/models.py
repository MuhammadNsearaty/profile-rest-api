from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from trips_api.models import Trip
import datetime

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, firstName,lastName,birthDay=None,gender='M',password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')
        if not birthDay:
            birthDay = datetime.date.today().isoformat()
        email = self.normalize_email(email)
        user = self.model(email=email, firstName=firstName,lastName=lastName,birthDay=birthDay,gender=gender)
        
        user.set_password(password)
        user.save(using=self._db)
        user.profilePicture = f'https://loremflickr.com/320/320/person?random={user.pk}'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, firstName='super',lastName='user',password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(verbose_name = 'email address',max_length=255, unique=True)
    firstName = models.CharField(max_length=255,default='')
    lastName = models.CharField(max_length=255,default='')
    birthDay = models.DateField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateField(default=datetime.date.today)
    profilePicture = models.URLField(max_length=200, null=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.firstName+self.lastName

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.firstName

    def __str__(self):
        """Return string representation of user"""
        return self.email
