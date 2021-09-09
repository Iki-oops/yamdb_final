from rest_framework import permissions

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'


class AuthorAdminModeratorObjectPermission(permissions.BasePermission):
    """
    Права доступа изменения объекта
    автора, администратора и модератора.
    """
    message = ('You must have author or admin '
               'or moderator rights to perform this action.')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.author == request.user:
            return True
        elif request.user.is_superuser:
            return True
        elif (
                request.user.is_authenticated
                and request.user.role == ADMIN):
            return True
        elif (
                request.user.is_authenticated
                and request.user.role == MODERATOR
        ):
            return True


class AdminPermissionOrReadOnlyPermission(permissions.BasePermission):
    """
    Права доступа администратора и
    чтения всеми пользователями.
    """
    message = 'You must have admin rights to perform this action.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        elif (
                request.user.is_authenticated
                and request.user.role == ADMIN
        ):
            return True


class AdminOnlyPermission(permissions.BasePermission):
    """Права доступа строго только администратора."""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated and request.user.role == ADMIN:
            return True
