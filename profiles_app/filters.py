from django_filters import filters, filterset

from profiles_app import models


class UserProfileFilter(filterset.FilterSet):
    birthday = filters.DateFromToRangeFilter()

    class Meta:
        model = models.UserProfile
        fields = ['gender', 'birthday']
