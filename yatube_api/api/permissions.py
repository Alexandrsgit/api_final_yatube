from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Кастомный класс для проверки прав на изменения данных."""

    def has_object_permission(self, request, view, obj):
        """Функция проверяет является ли пользователь автором."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
