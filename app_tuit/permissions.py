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
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user == obj.author or request.user.is_superuser
        else:
            return False

    # def has_object_permission(self, request, view, obj):
    #     if request.method in SAFE_METHODS:
    #         return True
    #     elif request.method in ['PUT', 'PATCH', 'DELETE']:
    #         print(f"User: {request.user}, Is Superuser: {request.user.is_superuser}, Author: {obj.author}")
    #         if request.user == obj.author or request.user.is_superuser:
    #             return True
    #         else:
    #             print("Permission denied")
    #     return False


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_superuser