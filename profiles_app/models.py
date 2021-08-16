import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, first_name, last_name, profile_picture, birthday, gender, password):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,
                          birthday=birthday, gender=gender, profile_picture=profile_picture)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, gender, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, first_name=first_name, last_name=last_name, password=password,
                                profile_picture=None, birthday=datetime.date.today(), gender=gender)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    password = models.CharField(max_length=128,
                                validators=[MinLengthValidator(8, message='Password must be at least 8 characters')])
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    birthday = models.DateField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateField(default=datetime.date.today)
    profile_picture = models.URLField(max_length=200, null=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    def get_full_name(self):
        """Retrieve full name for user"""
        return str(self.first_name) + str(self.last_name)

    def get_short_name(self):
        """Retrieve short name of user"""
        return str(self.first_name)

    def __str__(self):
        """Return string representation of user"""
        return self.email


class DeviceInfo(models.Model):
    uuid = models.CharField(max_length=100, unique=True)
    app_name = models.CharField(max_length=100)
    app_version = models.CharField(max_length=10)
    build_number = models.CharField(max_length=100)
    fcm_token = models.CharField(max_length=255, unique=True)
    os_version = models.CharField(max_length=100)
    os = models.CharField(max_length=10)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Device info"
        verbose_name_plural = "Devices info"

    def __str__(self):
        return f'{self.user} have {self.brand} device with {self.os} os'
