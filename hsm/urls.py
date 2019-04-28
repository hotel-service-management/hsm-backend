from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/booking/', include('booking.urls')),
    path('api/payment/', include('payment.urls')),
    path('api/review/', include('review.urls')),
]
