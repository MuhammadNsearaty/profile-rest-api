from django.contrib import admin


from hotels_api import models


admin.site.register(models.Place)
admin.site.register(models.Room)
admin.site.register(models.Hotel)
admin.site.register(models.Review)
admin.site.register(models.Location)

# Register your models here.
