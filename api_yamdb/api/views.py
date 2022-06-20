from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, viewsets
from reviews.models import Categories, Comments, Genres, Review, Title

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly, ReviewCommentViewSetPermissions
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentViewSetPermissions,)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentViewSetPermissions,)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, id=review_id, title=title)
        new_queryset = Comments.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)


class CategoriesViewSet(CreateListDestroyViewSet):
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Categories.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    pagination_class = pagination.LimitOffsetPagination
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer
