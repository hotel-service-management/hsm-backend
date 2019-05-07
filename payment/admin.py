from django.contrib import admin

from payment.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_date', 'payment_type', 'amount']
    list_per_page = 10
    list_filter = ['payment_date', 'payment_type', 'amount']


admin.site.register(Payment, PaymentAdmin)
