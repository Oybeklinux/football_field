from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        # Foydalanuvchining role ni tekshiramiz
        if request.user.role in ['admin', 'owner']:
            return True
        return False