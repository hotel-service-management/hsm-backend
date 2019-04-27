from rest_framework import generics, status, permissions
from rest_framework.response import Response

from booking.models import Booking, Room
from booking.serializers import BookingSerializer, RoomSerializer


class BookingView(generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve single Booking object
        :param request:
        :param args:
        :param kwargs:
        :return: Response
        """
        queryset = self.get_object()

        serializer = BookingSerializer(queryset, many=False)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({'success': True}, status=200)


class BookingsView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve single Room object
        :param request:
        :param args:
        :param kwargs:
        :return: Response
        """
        queryset = self.get_object()

        serializer = RoomSerializer(queryset, many=False)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({'success': True}, status=200)


class RoomsView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)
