from rest_framework import viewsets, permissions
from .models import Booking
from .serializers import BookingSerializer
from .permissions import EditIfOwnerOrAdmin

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [EditIfOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
