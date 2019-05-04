from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response

from order.models import Order, Service
from order.serializers import OrderSerializer, ServiceSerializer


class OrdersView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.annotate(
            service_cost=Sum('service__price')
        )

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = OrderSerializer(queryset, many=True)
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
