from django.contrib import admin

from booking.models import Booking, BookingDetail, Room, Privilege

# Register Booking
from order.models import Order


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


class PrivilegeInline(admin.StackedInline):
    model = Privilege
    extra = 1


class OrderInline(admin.StackedInline):
    model = Order
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BookingDetailAdmin(admin.ModelAdmin):
    inlines = [PrivilegeInline, OrderInline]


admin.site.register(BookingDetail, BookingDetailAdmin)


# Register Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'floor', 'type', 'price', 'room_number', ]
    list_per_page = 10

    search_fields = ['room_number']
    list_filter = ['floor', 'type']


admin.site.register(Room, RoomAdmin)
