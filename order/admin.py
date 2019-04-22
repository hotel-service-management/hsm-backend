from django.contrib import admin

from order.models import Order, Service, ServiceList

admin.site.register(Order)

admin.site.register(Service)

admin.site.register(ServiceList)
