from rest_framework import serializers

from booking.models import Booking
from booking.serializers import BookingSerializer
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)

    booking_id = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all(), write_only=True, source='booking')

    class Meta:
        model = Payment
        fields = '__all__'
