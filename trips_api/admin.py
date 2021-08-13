from django.contrib import admin

from trips_api import models

# Register your models here.

admin.site.register(models.Trip)
admin.site.register(models.Day)
