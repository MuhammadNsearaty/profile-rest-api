from django.contrib import admin

from planning_app import models


class PlaceAdmin(admin.ModelAdmin):
    filter_horizontal = ('properties',)


admin.site.register(models.Place, PlaceAdmin)
admin.site.register(models.GeoNameInfo)
admin.site.register(models.PlaceReview)
admin.site.register(models.Room)
admin.site.register(models.Property)
admin.site.register(models.Trip)
admin.site.register(models.Day)
admin.site.register(models.Activity)
