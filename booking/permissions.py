from rest_framework.permissions import BasePermission

class EditIfOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        # if request.user.
        # if request.method in ['GET', 'DELETE']
        #     return True  # POST, PUT, DELETE uchun faqat admin yoki owner bo'lishi kerak

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True  
        
        if request.user.role == 'owner' and obj.owner == request.user:
            return request.method in ['GET', 'DELETE']
            
        return False