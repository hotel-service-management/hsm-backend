from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer


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
