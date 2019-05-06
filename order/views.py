from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from booking.models import BookingDetail
from order.models import Order, Service
from order.serializers import OrderSerializer, ServiceSerializer


class OrdersView(generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.annotate(
            service_cost=Sum('service__price')
        )

    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            order = Order.objects.create(
                booking_detail=BookingDetail.objects.all().get(pk=data['booking_detail_id']), total_price=data['total_price'])
            order.service.add(*Service.objects.filter(pk__in=data['service']))
            serializer = OrderSerializer(order)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()

        serializer = OrderSerializer(queryset, many=False)
        return Response(serializer.data)


class OrderView(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.annotate(
            service_cost=Sum('service__price')
        )

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()

        serializer = OrderSerializer(queryset, many=False)
        return Response(serializer.data)


class ServicesView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class ServiceView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'booking__id'
    lookup_url_kwarg = 'pk'

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(booking__id=kwargs.get('pk'))

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
