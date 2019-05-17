from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from booking.models import Booking
from review.models import Review
from review.serializers import ReviewSerializer


class ReviewView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        try:
            if Booking.objects.get(pk=kwargs.get('pk')).owner.id != request.user.id:
                return Response({})
        except Booking.DoesNotExist:
            return Response({})

        queryset = self.get_object()

        serializer = ReviewSerializer(queryset, many=False)
        return Response(serializer.data)

    # def patch(self, request, *args, **kwargs):
    #     try:
    #         if Booking.objects.get(pk=kwargs.get('pk')).owner.id != request.user.id:
    #             return Response({})
    #     except Booking.DoesNotExist:
    #         return Response({})
    #
    #     super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({'success': True}, status=200)


class ReviewsView(generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        booking_id = data.pop('booking_id')

        if Booking.objects.get(pk=booking_id).owner.id != request.user.id:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            review = serializer.data.get('id')

            # Save review to booking
            booking = Booking.objects.get(pk=booking_id)
            booking.review_id = review
            booking.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_200_OK)
