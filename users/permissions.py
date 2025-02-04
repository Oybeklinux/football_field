from rest_framework.permissions import BasePermission

class UserPermission(BasePermission):
    """
    Faqat admin, owner va user CRUD amallarini bajara olishi mumkin.
    """
    def has_permission(self, request, view):
        # Foydalanuvchi autentifikatsiya qilingan bo‘lishi kerak
        if not request.user.is_authenticated:
            return False

        # Faqat admin, owner yoki user roliga ega bo'lganlar ruxsat olishi mumkin
        return request.user.role in ['admin']

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Faqat admin, owner yoki user roliga ega bo'lganlar ruxsat olishi mumkin
        return request.user.role in ['admin']