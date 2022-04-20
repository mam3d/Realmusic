from rest_framework import permissions

class IsFollowOwner(permissions.BasePermission):
    message = "you are not owner of this Follow"

    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user and request.user.is_authenticated)