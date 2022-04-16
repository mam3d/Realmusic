from rest_framework import permissions

class IsPlayListOwner(permissions.BasePermission):
    message = "you are not owner of this playlist"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj.user == request.user and request.user.is_authenticated)