from django.conf import settings
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from reviews.models import Categories, Comments, Genres, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    score = serializers.ChoiceField(choices=settings.SCORE)

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date', 'title'
        )

    def validate(self, data):
        user = self.context['view'].request.user
        title_id = self.context['view'].kwargs['title_id']
        if Review.objects.filter(
            title=get_object_or_404(Title, pk=title_id), author=user
        ).exists() and self.instance is None:
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв к этому произведению."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = (
            'id', 'text', 'author', 'pub_date', 'review'
        )


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        read_only_fields = ('id',)

    def get_rating(self, obj):
        try:
            rating = obj.reviews.aggregate(Avg('score'))
            return rating.get('score__avg')
        except TypeError:
            return None


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        model = Title
