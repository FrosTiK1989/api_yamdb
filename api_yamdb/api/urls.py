from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitlesViewSet)

app_name = 'api'

router = DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='reviews'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('', include(router.urls)),
]
