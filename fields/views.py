# from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.geos import Point
from rest_framework import viewsets

from booking.models import Booking
from .models import Field
from .serializers import FieldSerializer
from .permissions import EditIfOwnerOrAdmin
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.db.models import Q
from django.db.models import Case, When, Value
from django.db.models import Sum, BooleanField

# Maydonlar API
class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [EditIfOwnerOrAdmin] 

    def get_queryset(self):
        queryset = Field.objects.all()

        # Foydalanuvchi admin yoki owner bo'lsa, barcha maydonlarni ko'rsin
        if self.request.user.role in ['admin', 'owner']:
            return queryset

        
        # Vaqt filteri
        start_time = self.request.query_params.get("start_time")
        end_time = self.request.query_params.get("end_time")
        if start_time and end_time:
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)
            if start_time and end_time:
                start_time = make_aware(start_time)
                end_time = make_aware(end_time)
                
                not_ordered_fields = queryset.filter(
                    Q(bookings__isnull=True) 
                ).distinct()
                
                
                subquery = Booking.objects.annotate(
                    sign=Case(
                        When(
                            start_time__lte=start_time, end_time__gte=end_time, 
                            then=Value(1)
                        ),
                        When(
                            start_time__lte=start_time, end_time__gte=end_time,
                            then=Value(1)
                        ),
                        default=Value(0),
                        output_field=BooleanField()
                    )
                ).values('field_id').annotate(
                    sum_sign=Sum('sign')
                ).filter(sum_sign=0).values('field_id')
                
                fields_queryset = Field.objects.filter(id__in=subquery)
                queryset = fields_queryset.union(not_ordered_fields)

        # Lokatsiya bo‘yicha tartiblash
        # lat = self.request.query_params.get("lat")
        # lon = self.request.query_params.get("lon")

        # if lat and lon:
            # user_location = Point(float(lon), float(lat), srid=4326)  # GPS koordinatalari
            # queryset = queryset.annotate(distance=Distance("location", user_location)).order_by("distance")

        return queryset