from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.decorators import api_view, action
from django_filters import rest_framework as django_filters
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, status, filters
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from .models import Review, User, Category, Title, Genre
from .permissions import (
    AuthorAdminModeratorObjectPermission,
    AdminPermissionOrReadOnlyPermission,
    AdminOnlyPermission,
)
from .mixins import CategoryGenreModelMixin, TitleModelMixin
from .filters import TitleFilter
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    TitleSerializer,
    TitleCreateSerializer,
    GenreSerializer,
    UserSerializer,
    UserSerializerOrReadOnly
)

from django.db.models import Avg


@api_view(['POST'])
def send_confirmation_code(request):
    """Отправка письма с кодом подтверждения на почту."""
    email = request.data.get('email')
    email_split = email.split('@')
    username = email_split[0]
    user, created = User.objects.get_or_create(
        is_active=False,
        email=email,
        username=username,

    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Подтверждение регистрации',
        (f'Для получения токена и подтверждения регистрации сделайте '
         f'post-запрос со следующими параметрами:\n'
         f'Ваш email : {email}\n'
         f'Код подтверждения: {confirmation_code}'),
        'admin@api_yamdb.com',
        [email],
        fail_silently=False,
    )

    return Response({'email': email})


@api_view(['POST'])
def get_token(request):
    """Получение токена."""
    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(
            user=user,
            token=confirmation_code
    ):
        user.is_active = True
        user.save()

    def get_tokens_for_user(current_user):
        refresh = RefreshToken.for_user(current_user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    return_token = get_tokens_for_user(user)
    return Response(return_token)


class ReviewViewSet(viewsets.ModelViewSet):
    """API для работы с моделью отзывов"""

    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorAdminModeratorObjectPermission,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        queryset = title.reviews.order_by('id')
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """API для работы с моделью комментариев"""

    permission_classes = (
        AuthorAdminModeratorObjectPermission,
        IsAuthenticatedOrReadOnly
    )
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        queryset = review.comments.order_by('id')
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )


class CategoryViewSet(CategoryGenreModelMixin):
    """API для работы с моделью категорий"""

    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(CategoryGenreModelMixin):
    """API для работы с моделью жанров"""

    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class TitleViewSet(TitleModelMixin):
    """API для работы произведений"""

    queryset = Title.objects.all()
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_queryset(self):
        return Title.objects.order_by('id').annotate(
            rating=Avg('reviews__score')
        )

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    """API для работы пользователями"""

    lookup_field = 'username'
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """
        Запрос и возможность редактирования
         информации профиля пользователя.
        """
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
            serializer = UserSerializerOrReadOnly(
                user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
