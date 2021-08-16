from rest_framework import viewsets

from blogger_app import models
from blogger_app import serializers
from blogger_app import filters
from blogger_app import permissions


class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BlogSerializer
    permission_classes = (permissions.CreateOwnBlog,)
    ordering_fields = ['title', 'date']
    search_fields = ['title', 'tags__name']
    filterset_class = filters.BlogFilter
    queryset = models.Blog.objects.all()
