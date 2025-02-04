from rest_framework import serializers
# from django.contrib.gis.geos import Point
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

