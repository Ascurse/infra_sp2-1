from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.conf import settings


class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or request.method in SAFE_METHODS
        )


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == settings.IS_MODERATOR

    def has_object_permission(self, request, view, obj):
        return request.user.role == settings.IS_MODERATOR


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS


class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_superuser


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == settings.IS_ADMIN

    def has_object_permission(self, request, view, obj):
        return request.user.role == settings.IS_ADMIN
