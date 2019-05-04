from django.conf.urls import url
from django.urls import path

from order.views import OrdersView, OrderView

urlpatterns = [
    path('', OrdersView.as_view(), name='order_create'),
    path('<int:pk>/', OrderView.as_view(), name='order')
]
