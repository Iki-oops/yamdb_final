from rest_framework import serializers


from .models import Category, Title, Genre, Comment, Review, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категорий"""

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер жанров"""

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер произведений"""

    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField()

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер создания произведений"""

    category = serializers.SlugRelatedField(
        many=False,
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        is_review_exists = Review.objects.filter(
            title=title_id,
            author=user
        ).exists()
        if self.context['request'].method == 'POST' and is_review_exists:
            raise serializers.ValidationError('Второй отзыв оставить нельзя')
        return data

    class Meta:
        fields = (
            'id',
            'pub_date',
            'author',
            'text',
            'score'
        )
        read_only_fields = (
            'id',
            'pub_date',
            'author'
        )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер комментариев"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        read_only_fields = (
            'id',
            'pub_date',
            'author'
        )
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователей"""

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )
        model = User


class UserSerializerOrReadOnly(serializers.ModelSerializer):
    """Сериалайзер пользователей(чтение)"""

    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )
        model = User
