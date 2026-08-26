from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Разрешение позволяет изменять или удалять объект только его автору.
    """
    def has_object_permission(self, request, view, obj):
        # Проверка: является ли текущий пользователь создателем объекта
        return obj.creator == request.user