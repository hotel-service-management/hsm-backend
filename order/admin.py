from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from order.models import Order, Service


class OrderAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Order, OrderAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'title', 'price']


admin.site.register(Service, ServiceAdmin)
