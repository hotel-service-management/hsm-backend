from django.contrib import admin

from booking.models import Booking, BookingDetail, Room, Privilege
from order.models import Order

class BookingInline(admin.StackedInline):
    model = BookingDetail
    extra = 0


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'start_date', 'end_date', 'num_person', 'status']
    list_per_page = 10
    readonly_fields = ['id', 'owner', 'start_date', 'end_date', 'num_person']
    list_editable = ['status']

    fieldsets = (
        (
            'Start/End Date', {
                'fields': ('start_date', 'end_date')
            }
        ),
        (
            'Details', {
                'fields': ('num_person', 'owner')
            }
        ),
    )

    inlines = [BookingInline]

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
    list_display = ['id', 'booking', 'room', 'start_date', 'end_date']
    inlines = [PrivilegeInline, OrderInline]

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'floor', 'type', 'price', 'room_number']
    list_per_page = 10

    search_fields = ['room_number']
    list_filter = ['floor', 'type']

class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'title', 'status']

admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingDetail, BookingDetailAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Privilege, PrivilegeAdmin)
