from rest_framework import serializers
from .models import Booking
from hotels.serializers import HotelSerializer

class BookingSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'user', 'hotel', 'hotel_name', 'check_in_date', 'check_in_time',
            'check_out_date', 'check_out_time', 'no_of_persons', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'created_at', 'updated_at', 'hotel_name')

class BookingRetrieveSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True) # Nested serializer for hotel details

    class Meta:
        model = Booking
        fields = (
            'id', 'user', 'hotel', 'check_in_date', 'check_in_time',
            'check_out_date', 'check_out_time', 'no_of_persons', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'created_at', 'updated_at')