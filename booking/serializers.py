from rest_framework import serializers

from booking.models import Booking, BookingDetail, Room, Privilege
from review.serializers import ReviewSerializer


class RoomSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class BookingDetailSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room', write_only=True)

    def create(self, validated_data):
        return BookingDetail.objects.create(**validated_data)

    class Meta:
        model = BookingDetail
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    detail = BookingDetailSerializer(many=True, read_only=True)
    review = ReviewSerializer(read_only=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True, many=True)

    def to_representation(self, instance):
        representation = super(BookingSerializer, self).to_representation(instance)
        representation['start_date'] = instance.start_date.strftime("%d %B %Y")
        representation['end_date'] = instance.end_date.strftime("%d %B %Y")
        return representation

    def create(self, validated_data):
        rooms = validated_data.pop('room')

        booking = Booking.objects.create(**validated_data)

        for r in rooms:
            detail = BookingDetail.objects.create(room=r, booking=booking)
            booking.detail.add(detail)

        return booking

    class Meta:
        model = Booking
        fields = '__all__'


class PrivilegeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Privilege
        fields = '__all__'
