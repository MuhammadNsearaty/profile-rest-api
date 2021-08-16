from django.contrib import admin

from profiles_app import models

admin.site.register(models.UserProfile)
admin.site.register(models.DeviceInfo)
