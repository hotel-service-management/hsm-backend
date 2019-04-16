from datetime import date

from django.db import models

from booking.models import Booking


class Payment(models.Model):
    payment_date = models.DateField(null=date.today)
    amount = models.FloatField()

    payment_type_choice = (('01', 'Cash'), ('02', 'Credit Card'))
    payment_type = models.CharField(max_length=2, choices=payment_type_choice)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
