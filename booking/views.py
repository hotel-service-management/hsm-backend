import datetime

from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response

from booking.models import Booking, Room, BookingDetail, Privilege
from booking.serializers import BookingSerializer, RoomSerializer, BookingDetailSerializer, PrivilegeSerializer

# Booking
from users.models import User


class BookingView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()

        serializer = BookingSerializer(queryset, many=False)

        if queryset.owner.id != request.user.id:
            return Response({})

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({'success': True}, status=200)


class BookingsView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(owner=User.objects.get(email=request.user))
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data

        data['owner'] = request.user.id

        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_200_OK)


# Booking Detail
class BookingDetailView(generics.CreateAPIView):
    queryset = BookingDetail.objects.all()
    serializer_class = BookingDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        data = request.data

        if not kwargs.get('booking'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data['booking'] = kwargs.get('booking')

        serializer = BookingDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Room
class RoomView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()

        serializer = RoomSerializer(queryset, many=False)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({'success': True}, status=200)


class RoomsView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        start_date = request.query_params['start_date']
        end_date = request.query_params['end_date']

        booked = set(values['detail__room_id'] for values in Booking.objects.filter(
            start_date__lte=start_date, end_date__gte=end_date, status__in=[0, 1, 2]).values(
            'detail__room_id'))
        queryset = self.get_queryset().exclude(id__in=booked)
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Privilege
class PrivilegeView(generics.RetrieveAPIView):
    queryset = Privilege.objects.all().select_related('booking')
    serializer_class = PrivilegeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        try:
            booking_owner = BookingDetail.objects.get(pk=kwargs.get('pk')).booking.owner.id

            if request.user.id != booking_owner:
                return Response([], status=status.HTTP_401_UNAUTHORIZED)
        except BookingDetail.DoesNotExist:
            return Response([])

        queryset = self.get_queryset().filter(booking__id=kwargs.get('pk'))

        serializer = PrivilegeSerializer(queryset, many=True)
        return Response(serializer.data)
