import datetime

from django.db import models

from trip_pal_project import settings


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog_text = models.CharField(max_length=100000)
    date = models.DateField(default=datetime.date.today)
    # TODO make null False
    image = models.URLField(null=True)
    title = models.CharField(max_length=300)
    tags = models.ManyToManyField('Tag', related_name='blogs')

    def __str__(self):
        return self.title
