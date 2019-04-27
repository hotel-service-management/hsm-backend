from django.conf.urls import url
from django.urls import path

from booking.views import BookingView, BookingsView, RoomsView, RoomView

urlpatterns = [
    path('', BookingsView.as_view(), name='bookings'),
    path('<int:pk>/', BookingView.as_view(), name='booking'),
    path('room/', RoomsView.as_view(), name='rooms'),
    path('room/<int:pk>/', RoomView.as_view(), name='room'),

]
