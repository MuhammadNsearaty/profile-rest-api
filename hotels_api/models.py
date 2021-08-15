import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Location(models.Model):
    latitude = models.FloatField(null=False, default=0.0)
    longitude = models.FloatField(null=False, default=0.0)
    cityName = models.CharField(max_length=15)


class HotelReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    hotelId = models.ForeignKey(
        'Hotel',
        on_delete=models.CASCADE
    )
    reviewText = models.CharField(max_length=2000)
    overallRating = 0.0


class PlaceReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    placeId = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE
    )
    reviewText = models.CharField(max_length=5000)
    overallRating = 0.0


class Hotel(models.Model):
    name = models.CharField(max_length=10)
    # location = models.ForeignKey(
    #     'Location',
    #     on_delete=models.DO_NOTHING,
    # )
    latitude = models.FloatField(null=False, default=0.0)
    longitude = models.FloatField(null=False, default=0.0)
    cityName = models.CharField(max_length=15)

    distance = models.FloatField(null=False, default=0.0)
    guestrating = models.FloatField(null=False, default=0.0,
                                    validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    kinds = models.CharField(max_length=1000, default='')
    description = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    # TODO make null False
    image = models.URLField(max_length=200, null=True)


class Place(models.Model):
    name = models.CharField(max_length=10)
    # location = models.ForeignKey(
    #     'Location',
    #     on_delete=models.DO_NOTHING,
    # )
    latitude = models.FloatField(null=False, default=0.0)
    longitude = models.FloatField(null=False, default=0.0)
    cityName = models.CharField(max_length=15)
    
    distance = models.FloatField(null=False, default=0.0)
    guestrating = models.FloatField(null=False, default=0.0,
                                    validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    kinds = models.CharField(max_length=1000, default='')
    address = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')
    # TODO make null False
    image = models.URLField(max_length=200, null=True)


class Room(models.Model):
    hotelId = models.ForeignKey(
        'Hotel',
        on_delete=models.CASCADE
    )
    checkinDate = models.DateTimeField()
    checkoutDate = models.DateTimeField()
    details = models.CharField(max_length=1000)

# class Restaurant(Place,Bookable):
#     checkinDate = models.DateTimeField()
#     orderMenu = []#list(Order())
#     # @override
#     def makeAnAppointment():
#         pass


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog_text = models.CharField(max_length=100000)
    date = models.DateField(default=datetime.date.today)
    # TODO make null False
    image = models.URLField(null=True)
    title = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)

# class BlogHasTag(models.Model):
    # blog_id = models.ForeignKey('Blog', on_delete=models.CASCADE)
    # tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE)
    #
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['blog_id', 'tag_id'], name='uniqueness')
    #     ]
