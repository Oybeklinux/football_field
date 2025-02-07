from flask import request
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
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Sin, Radians

# Maydonlar API
class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [EditIfOwnerOrAdmin] 


    def get_queryset(self):
        queryset = Field.objects.all()

        # Foydalanuvchi admin bo'lsa, barcha maydonlarni ko'rsin
        if self.request.user.role == 'admin':
            return queryset
        
        # Foydalanuvchi owner o'zini maydonlarini ko'rsin
        if self.request.user.role == 'owner':
            return queryset.filter(owner=self.request.user)

        
        # Foydalanuvchi user bo'lsa, vaqt oralig'ida, masofa bo'yicha tartiblangan holda ko'sin
        start_time = self.request.query_params.get("start_time")
        end_time = self.request.query_params.get("end_time")
        if start_time and end_time:
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)
            if start_time and end_time:
                start_time = make_aware(start_time)
                end_time = make_aware(end_time)
                
                not_rented_fields = queryset.filter(
                    Q(bookings__isnull=True) 
                ).distinct()
                
                
                fields_id = Booking.objects.annotate(
                    sign=Case(
                        When(
                            start_time__gte=start_time, end_time__lte=start_time, 
                            then=Value(1)
                        ),
                        When(
                            start_time__gte=end_time, end_time__lte=end_time,
                            then=Value(1)
                        ),
                        default=Value(0),
                        output_field=BooleanField()
                    )
                ).values('field_id').annotate(
                    sum_sign=Sum('sign')
                ).filter(sum_sign=0).values('field_id')
                
                fields_queryset = Field.objects.filter(id__in=fields_id)
                # queryset = fields_queryset.union(not_rented_fields)

        # Lokatsiya bo‘yicha tartiblash
        lat = float(self.request.query_params.get("lat"))
        lon = float(self.request.query_params.get("lon"))

        if lat and lon:            
            distance_expression = self.get_expr_of_nearest_locations(lat, lon)
            fields_queryset = fields_queryset.annotate(distance=distance_expression)
            not_rented_fields = not_rented_fields.annotate(distance=distance_expression)
            queryset = fields_queryset.union(not_rented_fields)
            queryset.order_by("distance")
        
        
        return queryset

    @staticmethod
    def get_expr_of_nearest_locations(user_lat, user_lon):
        # Radius of the Earth in kilometers
        R = 6371

        # Haversine formula
        distance_expr = ExpressionWrapper(
            R * ACos(
                Cos(Radians(user_lat)) * Cos(Radians(F('lat'))) *
                Cos(Radians(F('long')) - Radians(user_lon)) +
                Sin(Radians(user_lat)) * Sin(Radians(F('lat')))
            ),
            output_field=FloatField()
        )
        return distance_expr