from django.contrib import admin

from trips_api import models


class DayAdmin(admin.ModelAdmin):
    filter_horizontal = ('hotels', 'places')


admin.site.register(models.Trip)
admin.site.register(models.Day, DayAdmin)
