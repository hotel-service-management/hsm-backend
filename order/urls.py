from django.conf.urls import url
from django.urls import path

from order.views import OrdersView, OrderView, ServiceView, ServicesView

urlpatterns = [
    path('', OrdersView.as_view(), name='order_create'),
    path('<int:pk>/', OrderView.as_view(), name='order'),
    path('service/', ServicesView.as_view(), name='services'),
    path('service/<int:pk>/', ServiceView.as_view(), name='service')
]
