from django.contrib.auth import get_user_model
from django.db import models

from .validators import my_year_validator


User = get_user_model()


class Category(models.Model):
    """Модель категорий"""

    name = models.CharField(
        verbose_name='Категория',
        max_length=100
    )
    slug = models.SlugField(
        verbose_name='Ссылка',
        max_length=30,
        unique=True
    )

    class Meta:
        ordering = ['id', ]
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров"""

    name = models.CharField(max_length=50, verbose_name='Жанр')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='Ссылка')

    class Meta:
        ordering = ['id', ]
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'


class Title(models.Model):
    """Модель произведений"""

    name = models.CharField(
        verbose_name='Произведение',
        max_length=100
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        null=True,
        blank=True,
        validators=[my_year_validator,]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='Категория'
    )
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre'
    )

    class Meta:
        ordering = ['id', ]
        verbose_name_plural = 'Произведения'
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель жанров произведений"""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )


class Review(models.Model):
    """Модель отзыва"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )
    score = models.IntegerField()

    rating = models.IntegerField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
