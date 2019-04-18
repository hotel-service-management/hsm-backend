from django.db import models

from users.models import User


class Booking(models.Model):
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    num_person = models.IntegerField(null=False, default=1)
    stay_date = models.IntegerField(null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Room(models.Model):
    price = models.FloatField(default=0)
    floor = models.IntegerField(default=1)

    type_choice = (('01', 'Deluxe'), ('02', 'Family'), ('03', 'Suite'))
    type = models.CharField(max_length=2, choices=type_choice, null=True)


class BookingDetail(models.Model):
    class Meta:
        db_table = 'booking_detail'

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
