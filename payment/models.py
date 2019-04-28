from datetime import date

from django.db import models

from booking.models import Booking


class Payment(models.Model):
    payment_date = models.DateField(default=date.today)
    amount = models.FloatField()

    payment_type_choice = (('01', 'Cash'), ('02', 'Credit Card'))
    payment_type = models.CharField(max_length=2, choices=payment_type_choice)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return "(%s/%s) %s" % (self.id, self.booking.id, self.amount)
