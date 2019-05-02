from rest_framework import serializers

from booking.models import Booking, BookingDetail, Room


class RoomSerializer(serializers.ModelSerializer):
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

    def to_representation(self, instance):
        representation = super(BookingSerializer, self).to_representation(instance)
        representation['start_date'] = instance.start_date.strftime("%d %B %Y")
        representation['end_date'] = instance.end_date.strftime("%d %B %Y")
        return representation

    class Meta:
        model = Booking
        fields = '__all__'
