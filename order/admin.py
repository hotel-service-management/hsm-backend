from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from order.models import Order, Service


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking_detail', 'total_price']
    readonly_fields = ['total_price']

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def save_model(self, request, obj, form, change):
        """ NOTES: MUST DOUBLE-SAVE TO REALLY UPDATE TOTAL_PRICE """
        super().save_model(request, obj, form, change)
        Order.objects.filter(pk=obj.id).update(total_price=sum([i.price for i in Order.objects.get(pk=obj.id).service.all()]))

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'title', 'price']
    list_filter = ['type']
    search_fields = ['title']

admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
