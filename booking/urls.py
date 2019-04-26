from django.conf.urls import url
from django.urls import path

from booking.views import BookingView, BookingsView

urlpatterns = [
    path('', BookingsView.as_view(), name='bookings'),
    path('<int:pk>/', BookingView.as_view(), name='booking')
]
