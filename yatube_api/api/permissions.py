from django.core.exceptions import PermissionDenied
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Проверяет что пользователь является автором."""
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        
        if obj.author != request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        return obj.author == request.user