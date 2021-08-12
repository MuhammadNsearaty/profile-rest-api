from django.contrib import admin

# Register your models here.

from trips_api import models


admin.site.register(models.Trip)
admin.site.register(models.Day)