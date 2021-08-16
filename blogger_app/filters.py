from functools import reduce

from django_filters import filters, filterset
from blogger_app import models


class BlogFilter(filterset.FilterSet):
    date = filters.DateFromToRangeFilter()
    tags = filters.BaseCSVFilter(
        field_name='tags',
        method='filter_tags',
    )

    def filter_tags(self, queryset, name, value):
        if value:
            return reduce(lambda x, y: x & y, [models.Blog.objects.filter(tags=tag) for tag in value])
        return models.Blog.objects.all(),

    class Meta:
        model = models.Blog
        fields = ['date', 'tags']
