from django.contrib import admin
from .models import Review, Comment, Category, Title, Genre


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Страница отзывов в админке"""

    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'pub_date',
        'score',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Страница комментариев в админке"""

    list_display = (
        'pk',
        'review',
        'author',
        'text',
        'pub_date'
    )

    search_fields = ('text', 'author')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    list_display_links = ('pk', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category',)
    list_display_links = ('pk', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
