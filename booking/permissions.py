from rest_framework.permissions import BasePermission, SAFE_METHODS

class BookingPermission(BasePermission):
    """
    Admin barcha bookinglarni ko‘rishi, yaratishi, o‘zgartirishi va o‘chirishi mumkin.
    Owner faqat o‘z bookinglarini ko‘rishi va o‘chirishi mumkin.
    Oddiy foydalanuvchilar hech narsa qila olmaydi.
    """

    def has_permission(self, request, view):
        """Foydalanuvchi tizimga kirganligini tekshiramiz"""
        if not request.user or request.user.is_anonymous:
            return False  # Agar foydalanuvchi anonim bo‘lsa, ruxsat yo‘q
        
        if request.user.role == 'admin':
            return True
        
        
        # POST, PUT, PATCH, DELETE so‘rovlari faqat admin uchun ruxsat etilgan
        if request.method in ['GET', 'DELETE'] and request.user.role == 'owner':
            return True
        
        return False  # Oddiy userlar hech narsa qila olmaydi

    def has_object_permission(self, request, view, obj):
        """Obyekt bo‘yicha ruxsatlarni tekshiramiz"""
        if not request.user or request.user.is_anonymous:
            return False  # Agar foydalanuvchi anonim bo‘lsa, ruxsat yo‘q
        
        if request.user.role == 'admin':
            return True  # Admin barcha bookinglarni boshqara oladi

        # owner hammasini ko'ra oladi. Va o'zinikini o'chira oladi
        if request.user.role == 'owner':
            if request.method == 'GET':
                return True
            elif request.method == 'DELETE' and obj.user == request.user:
                return True
        
        return False  # Oddiy userlar hech narsa qila olmaydi
