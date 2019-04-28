from rest_framework import serializers

from booking.models import Booking
from booking.serializers import BookingSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)

    booking_id = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all(), write_only=True, source='booking')

    class Meta:
        model = Review
        fields = '__all__'
