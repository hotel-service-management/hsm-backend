from rest_framework import generics, permissions, status
from rest_framework.response import Response

from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_200_OK)


class PaymentsView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView, generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()

        serializer = PaymentSerializer(queryset, many=False)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({'success': True}, status=200)
