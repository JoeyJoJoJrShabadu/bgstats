from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.poster == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.action =='retrieve' or request.user.is_admin
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj == request.user 