from rest_framework import serializers

from booking.models import Booking, BookingDetail, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BookingDetailSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = BookingDetail
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    detail = BookingDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
