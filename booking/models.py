from django.db import models

from users.models import User


class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    num_person = models.IntegerField(null=False, default=1, verbose_name='Person Count')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'bookings'

    def __str__(self):
        return "(%s) %s" % (self.id, self.owner)


class Room(models.Model):
    price = models.FloatField(default=0)
    floor = models.IntegerField(default=1)
    room_number = models.CharField(max_length=10, blank=True, null=True)

    type_choice = (('01', 'Deluxe'), ('02', 'Family'), ('03', 'Suite'))
    type = models.CharField(max_length=2, choices=type_choice, null=True)

    def __str__(self):
        return "(%s) %s" % (self.room_number, self.get_type_display())


class BookingDetail(models.Model):
    class Meta:
        db_table = 'booking_detail'
        verbose_name = 'Booking Detail'
        verbose_name_plural = 'Booking Details'

    booking = models.ForeignKey(Booking, related_name='detail', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)

    def __str__(self):
        return "(%s %s) %s" %(self.booking_id, self.booking.owner, self.room.room_number)


class Privilege(models.Model):
    booking = models.ForeignKey(BookingDetail, related_name='booking_detail', on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    detail = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name='Used ?')

    class Meta:
        db_table = 'privilege'
