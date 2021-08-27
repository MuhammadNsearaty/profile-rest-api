import datetime

from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from profiles_app.models import UserProfile

from blogger_app import models
from blogger_app import serializers
from blogger_app import filters
from blogger_app import permissions

from shared.permissions import ModeratedByAdminOnly


def _truncate(dt):
    return dt.date()


class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.OwnerOrAdmin,)
    ordering_fields = ['title', 'date', 'likes_count']
    search_fields = ['title', 'tags__name']
    filterset_class = filters.BlogFilter
    queryset = models.Blog.objects.annotate(likes_count=Count('likes'))

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BlogMiniSerializer
        if self.action == 'blogger_of_week':
            return serializers.UserProfileSerializer
        if self.action == 'like':
            return serializers.UserLikeSerializer
        return serializers.BlogSerializer

    @action(methods=['GET'], url_path='blogger-of-week', detail=False,
            filterset_class=None, ordering_fields=[], search_fields=[])
    def blogger_of_week(self, request):
        qs = models.UserLikeBlog.objects.filter(
            date__gte=_truncate(datetime.datetime.now() - datetime.timedelta(days=7)),
            date__lt=_truncate(datetime.datetime.now() + datetime.timedelta(days=1))).values_list(
            'blog__user').annotate(
            likes_count=Count('blog__user')).order_by('-likes_count').filter(likes_count__gte=5)
        qs = UserProfile.objects.filter(pk__in=qs.values_list('blog__user'))
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], url_path='like',
            detail=True,
            serializer_class=serializers.UserLikeSerializer,
            filterset_class=None,
            ordering_fields=[],
            search_fields=[])
            
    def like(self, request, pk):
        serializer: serializers.UserLikeSerializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            blog = self.get_object()
            headers = self.get_success_headers(serializer.data)
            if serializer.validated_data['action'] == 1:
                like, created = models.UserLikeBlog.objects.get_or_create(blog=blog, user=request.user)
                if created:
                    return Response({'message': f'you have liked \"{blog}\"'},
                                    status=status.HTTP_201_CREATED, headers=headers)
                else:
                    return Response({'message': f'you have liked \"{blog}\"'},
                                    status=status.HTTP_200_OK, headers=headers)
            else:
                try:
                    models.UserLikeBlog.objects.get(blog=blog, user=request.user).delete()
                    return Response({'message': f'you have disliked \"{blog}\"'},
                                    status=status.HTTP_200_OK, headers=headers)
                except ObjectDoesNotExist:
                    return Response({'message': f'you have disliked \"{blog}\"'},
                                    status=status.HTTP_200_OK, headers=headers)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (ModeratedByAdminOnly, )
    ordering_fields = ['name', 'blog_count']
    search_fields = ['name', 'description']
    filterset_class = filters.TagFilter
    queryset = models.Tag.objects.annotate(blog_count=Count('blogs'))


class LikesViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = models.UserLikeBlog.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.UserLikeBlogSerializer
    filterset_class = filters.LikesFilter
    ordering_fields = ['date', 'blog__likes']
