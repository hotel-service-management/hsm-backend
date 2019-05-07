from django.conf.urls import url
from django.urls import path, include

from .views import RegistrationAPIView, UserRetrieveUpdateAPIView, LoginAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view(), name='user_info'),
    url(r'^register/?$', RegistrationAPIView.as_view(), name='register'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
