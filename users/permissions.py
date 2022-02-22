from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.account.owner.id == request.user.id

class UserPermissions(permissions.BasePermission):
    def has_object_permission(self, request, _, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.id == request.user.id:
            if request.method == 'DELETE':
                return False
            return True

        if request.user.account.owner.id == request.user.id:
            return True

        return False
