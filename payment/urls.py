from django.conf.urls import url
from django.urls import path

from payment.views import PaymentView, PaymentsView

urlpatterns = [
    path('', PaymentView.as_view(), name='payment_create'),
    path('<int:pk>/', PaymentsView.as_view(), name='payment')
]
