import datetime

from django.contrib import admin

from booking.models import Booking, BookingDetail, Room, Privilege, PrivilegeType, RoomType
from order.models import Order
from payment.models import Payment

class BookingInline(admin.StackedInline):
    model = BookingDetail
    extra = 0
    readonly_fields = ['total_price']

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

class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0

class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'start_date', 'end_date', 'nights', 'total_price', 'num_person', 'status', 'check_in', 'check_out']
    list_per_page = 10
    search_fields = ['id']
    list_filter = ['status', 'start_date', 'end_date']
    list_editable = ['status']
    raw_id_fields = ['owner']

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
        (
            'Status', {
                'fields': ('status', 'check_in', 'check_out')
            }
        ),
    )

    inlines = [BookingInline, PaymentInline]

    def save_model(self, request, obj, form, change):
        """ NOTES: MUST DOUBLE-SAVE TO REALLY UPDATE TOTAL_PRICE """
        if obj.status == 0:
            obj.check_in = None
            obj.check_out = None

        elif obj.status == 1:
            if obj.check_in is None:
                obj.check_in = datetime.datetime.now()
            obj.check_out = None

        elif obj.status == 2:
            if obj.check_out is None:
                obj.check_out = datetime.datetime.now()

        for i in BookingDetail.objects.filter(booking_id=obj.id):
            i.total_price = i.get_total_price()
            i.save()

        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'start_date', 'end_date', 'owner', 'check_in', 'check_out']
        return ['status', 'check_in', 'check_out']

class BookingDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'room', 'start_date', 'end_date', 'nights', 'total_price']
    raw_id_fields = ['booking']
    inlines = [PrivilegeInline, OrderInline]

    def save_model(self, request, obj, form, change):
        """ NOTES: MUST DOUBLE-SAVE TO REALLY UPDATE TOTAL_PRICE """
        super().save_model(request, obj, form, change)
        BookingDetail.objects.filter(pk=obj.id).update(
            total_price=BookingDetail.objects.get(pk=obj.id).get_total_price()
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'booking', 'total_price']
        return ['total_price']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'floor', 'type', 'price', 'room_number']
    list_per_page = 10

    search_fields = ['room_number']
    list_filter = ['floor', 'type']

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'amount', 'min_price', 'max_price', 'available_today', 'min_price_available', 'max_price_available']
    search_fields = ['title']

class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'type', 'title', 'status']
    list_filter = ['type', 'status']

class PrivilegeTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']

admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingDetail, BookingDetailAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(PrivilegeType, PrivilegeTypeAdmin)
admin.site.register(Privilege, PrivilegeAdmin)
