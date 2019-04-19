from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# from users.views import RegistrationAPIView
# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    # path('api/register/', RegistrationAPIView.as_view(), name='register'),
]