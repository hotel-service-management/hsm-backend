from django.contrib import admin

from booking.models import Booking, BookingDetail, Room


# Register Booking
class BookingInline(admin.StackedInline):
    model = BookingDetail
    extra = 0


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_date', 'end_date', 'num_person', 'owner']
    list_per_page = 10

    fieldsets = (
        (
            'Start/End Date', {
                'fields': ('start_date', 'end_date',)
            }
        ),
        (
            'Details', {
                'fields': ('num_person', 'owner',)
            }
        ),
    )

    inlines = [BookingInline]


admin.site.register(Booking, BookingAdmin)


class BookingDetailAdmin(admin.ModelAdmin):
    pass


admin.site.register(BookingDetail, BookingDetailAdmin)


# Register Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'floor', 'type', 'price', ]
    list_per_page = 10

    search_fields = ['room_number']
    list_filter = ['floor', 'type']


admin.site.register(Room, RoomAdmin)
