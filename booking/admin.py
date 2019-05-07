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
    list_display = ['id', 'owner', 'start_date', 'end_date', 'nights', 'total_price', 'num_person', 'status']
    list_per_page = 10
    search_fields = ['id']
    list_filter = ['status', 'start_date', 'end_date']
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
        (
            'Status', {
                'fields': ('status',)
            }
        ),
    )

    inlines = [BookingInline, PaymentInline]

    def save_model(self, request, obj, form, change):
        """ NOTES: MUST DOUBLE-SAVE TO REALLY UPDATE TOTAL_PRICE """
        super().save_model(request, obj, form, change)
        for i in BookingDetail.objects.filter(booking_id=obj.id):
            i.total_price = i.get_total_price()
            i.save()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'start_date', 'end_date', 'owner']
        return []

class BookingDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'room', 'start_date', 'end_date', 'nights', 'total_price']
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

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'amount', 'min_price', 'max_price', 'available_today', 'min_price_available', 'max_price_available']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'floor', 'type', 'price', 'room_number']
    list_per_page = 10

    search_fields = ['room_number']
    list_filter = ['floor', 'type']

class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'title', 'detail', 'status']

admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingDetail, BookingDetailAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(PrivilegeType)
admin.site.register(Privilege, PrivilegeAdmin)
