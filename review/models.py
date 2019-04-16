from django.db import models

from booking.models import Booking


class Review(models.Model):
    score = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)
