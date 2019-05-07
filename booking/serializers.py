from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from booking.models import Booking, BookingDetail, Room, Privilege, RoomType
from order.serializers import OrderSerializer
from review.serializers import ReviewSerializer


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    type = RoomTypeSerializer()

    class Meta:
        model = Room
        fields = '__all__'


class BookingDetailSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room', write_only=True)
    order_set = OrderSerializer(read_only=True, many=True)

    def create(self, validated_data):
        return BookingDetail.objects.create(**validated_data)

    class Meta:
        model = BookingDetail
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    detail = BookingDetailSerializer(many=True, read_only=True)
    review = ReviewSerializer(read_only=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True, many=True)
    night = serializers.IntegerField(source='nights', read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    status_id = serializers.IntegerField(source='status', write_only=True, required=False)

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

    def validate(self, data):
        if 'start_date' in data.keys() and 'end_date' in data.keys():
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError("Check-in Date must be after Check-out Date")
        return data

    class Meta:
        model = Booking
        fields = '__all__'


class PrivilegeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Privilege
        fields = '__all__'
