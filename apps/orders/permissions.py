from rest_framework.permissions import BasePermission, SAFE_METHODS


class AllowCreateOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return (request.method in SAFE_METHODS or request.user and
                request.user.is_authenticated)
