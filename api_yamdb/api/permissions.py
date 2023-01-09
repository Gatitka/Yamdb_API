from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Методы GET, HEAD и OPTIONS доступны для всех пользователей (и анонимов).
    Добавлять, редактировать и удалять (методы POST, PUT, PATCH, DELETE)
    записи могут только пользователи с ролью 'admin' или суперюзеры.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.auth:
            return request.user.role == 'admin' or request.user.is_superuser
        return False


class IsAdmin(permissions.BasePermission):
    """
    Выполнение запросов запрещено для всех, кроме пользователей
    с ролью 'admin' или суперюзеров.
    """
    def has_permission(self, request, view):
        if request.auth:
            return request.user.role == 'admin' or request.user.is_superuser
        return False
