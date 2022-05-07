from rest_framework import permissions

class UnauthenticatedOnly(permissions.BasePermission):
    message = "this view is unauthenticated only"

    def has_permission(self, request, view):
        return not request.user.is_authenticated