# from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.geos import Point
from rest_framework import viewsets
from .models import Field
from .serializers import FieldSerializer
from .permissions import EditIfOwnerOrAdmin

# Maydonlar API
class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [EditIfOwnerOrAdmin] 

    # def get_queryset(self):
    #     queryset = Field.objects.all()
    #     # latitude = self.request.query_params.get('latitude')
    #     # longitude = self.request.query_params.get('longitude')
    #     start_time = self.request.query_params.get('start_time')
    #     end_time = self.request.query_params.get('end_time')

    #     # # Eng yaqin maydonlar bo'yicha filterlash
    #     # if latitude and longitude:
    #     #     user_location = Point(float(longitude), float(latitude), srid=4326)
    #     #     queryset = queryset.annotate(distance=Distance('location', user_location)).order_by('distance')

    #     # Bron qilinmagan maydonlarni filterlash
    #     if start_time and end_time:
    #         queryset = queryset.exclude(bookings__start_time__lt=end_time, bookings__end_time__gt=start_time)

    #     return queryset
