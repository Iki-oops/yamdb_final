from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    send_confirmation_code,
    CategoryViewSet,
    TitleViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
    get_token,
    UserViewSet
)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comment'
)
router.register('users', UserViewSet, basename='User')

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/email/',
        send_confirmation_code,
        name='send_confirmation_code'
    ),
    path(
        'v1/auth/token/',
        get_token,
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
