from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_perm(self, request, view, obj):
        if request.method != 'GET':
            return False
        return obj.owner == request.user
