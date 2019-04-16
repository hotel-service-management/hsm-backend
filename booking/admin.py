from django.contrib import admin

from booking.models import Booking, BookingDetail, Room

admin.site.register(Booking)

admin.site.register(BookingDetail)

admin.site.register(Room)