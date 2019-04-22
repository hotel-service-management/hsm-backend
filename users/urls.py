from django.conf.urls import url
from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/register/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view(), name='auth_login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
