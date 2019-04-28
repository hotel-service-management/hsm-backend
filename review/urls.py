from django.conf.urls import url
from django.urls import path

from review.views import ReviewView, ReviewsView

urlpatterns = [
    path('', ReviewsView.as_view(), name='reviews'),
    path('<int:pk>/', ReviewView.as_view(), name='review'),
]
