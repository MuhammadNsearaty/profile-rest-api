from django.db.models import Count

from rest_framework import viewsets

from blogger_app import models
from blogger_app import serializers
from blogger_app import filters
from blogger_app import permissions

from shared.permissions import ModeratedByAdminOnly


class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BlogSerializer
    permission_classes = (permissions.OwnerOrAdmin,)
    ordering_fields = ['title', 'date']
    search_fields = ['title', 'tags__name']
    filterset_class = filters.BlogFilter
    queryset = models.Blog.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (ModeratedByAdminOnly, )
    ordering_fields = ['name', 'blogs_count']
    search_fields = ['name', 'description']
    queryset = models.Tag.objects.annotate(blogs_count=Count('blogs')).all()
