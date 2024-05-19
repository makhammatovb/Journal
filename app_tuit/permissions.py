from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST' and request.user.is_authenticated:
            return True
        return False


    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE'] and request.user == obj.user:
            return True
        else:
            return False


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_superuser