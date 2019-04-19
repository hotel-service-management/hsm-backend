from django.contrib import admin

from order.models import Order, Service, ServiceList, Food, FoodList

admin.site.register(Order)

admin.site.register(Service)

admin.site.register(ServiceList)

admin.site.register(Food)

admin.site.register(FoodList)
