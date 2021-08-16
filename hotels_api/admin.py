from django.contrib import admin

from hotels_api import models


class BlogAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags', )


admin.site.register(models.Place)
admin.site.register(models.Room)
admin.site.register(models.Hotel)
admin.site.register(models.HotelReview)
admin.site.register(models.PlaceReview)
admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Tag)
