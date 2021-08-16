from django.contrib import admin

from blogger_app import models


class BlogAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags', )


admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Tag)
