from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Categories(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        max_length=256,
        verbose_name='URL категории',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL жанра',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        verbose_name='Жанр',
        blank=True,
    )
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')
    name = models.CharField(max_length=256, db_index=True)
    rating = models.IntegerField(
        null=True,
        default=None,
    )
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.PositiveSmallIntegerField(choices=settings.SCORE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
