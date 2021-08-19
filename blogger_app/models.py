import datetime

from django.db import models

from trip_pal_project import settings


class Tag(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=250)
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs')
    blog_text = models.CharField(max_length=2500)
    date = models.DateField(default=datetime.date.today)
    # TODO make null False
    image = models.URLField(null=True)
    title = models.CharField(max_length=30)
    tags = models.ManyToManyField('Tag', related_name='blogs')

    def __str__(self):
        return self.title


class UserLikeBlog(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_likes')
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.user} likes {self.blog}'
