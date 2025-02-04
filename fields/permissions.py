from rest_framework.permissions import BasePermission

class EditIfOwnerOrAdmin(BasePermission):
    """
    Ruxsat: faqat admin yoki owner foydalanuvchiga PUT, DELETE, POST so‘rovlarini yuborishga ruxsat beradi.
    """

    def has_permission(self, request, view):
        """
        Bu metod umumiy ruxsatlarni tekshiradi. 
        GET so'rovlarini barcha foydalanuvchilar uchun ruxsat beradi.
        POST, PUT, DELETE uchun faqat admin yoki owner bo'lishi kerak.
        """
        if request.method == 'GET':
            return True  # GET so'rovlari uchun hech qanday cheklov yo'q
        if request.user.role in ['admin', 'owner']:
            return True  # POST, PUT, DELETE uchun faqat admin yoki owner bo'lishi kerak

        return False

    def has_object_permission(self, request, view, obj):
        """
        Bu metod ob'ektga oid ruxsatlarni tekshiradi.
        admin har qanday fieldni o'zgartirishi yoki o'chirishi mumkin,
        owner faqat o'ziga tegishli fieldni o'zgartirishi yoki o'chirishi mumkin.
        """
        if request.method == 'GET':
            return True
        
        if request.user.role == 'admin':
                return True  # Admin har qanday fieldni o'zgartirishi mumkin
            
        if request.method in ['PUT', 'DELETE']:            
            if request.user.role == 'owner' and obj.owner == request.user:
                return True  # Owner faqat o'ziga tegishli fieldni o'zgartirishi mumkin
            
        return False