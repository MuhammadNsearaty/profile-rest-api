from functools import reduce

from django.core.exceptions import ValidationError
from django.forms import forms
from django_filters import filters, filterset

from blogger_app import models


class BlogFilterForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        properties = cleaned_data.get("tags")
        if properties:
            for value in properties:
                try:
                    int(value)
                except ValueError:
                    raise ValidationError({'tags': 'all values must be integers'})
        return cleaned_data


class BlogFilter(filterset.FilterSet):
    date = filters.DateFromToRangeFilter()
    tags = filters.BaseCSVFilter(
        field_name='tags',
        method='filter_tags',
    )
    likes_count = filters.RangeFilter(label='Likes Count')

    def filter_tags(self, queryset, name, value):
        if self.is_valid():
            if value:
                return reduce(lambda x, y: x & y, [queryset.filter(tags=tag) for tag in value])
            return queryset

    class Meta:
        model = models.Blog
        form = BlogFilterForm
        fields = ['date', 'tags', 'user', 'likes_count']


class TagFilter(filterset.FilterSet):
    blog_count = filters.RangeFilter(label='Blog Count')

    class Meta:
        model = models.Tag
        fields = []


class LikesFilter(filterset.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = models.UserLikeBlog
        fields = ['date', 'user', 'blog']
