from django.db import models

from users.models import User


class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    num_person = models.IntegerField(null=False, default=1, verbose_name='Person Count')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    status_choices = (
        (0, 'Reserved'),
        (1, 'Checked In'),
        (2, 'Checked Out')
    )
    status = models.SmallIntegerField(choices=status_choices, verbose_name='Booking Status', default=0)

    class Meta:
        db_table = 'bookings'

    def nights(self):
        return (self.end_date - self.start_date).days

    def total_price(self):
        return sum([i.room.price * self.nights() for i in BookingDetail.objects.all().filter(booking=self.id)])

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

    def start_date(self):
        return self.booking.start_date

    def end_date(self):
        return self.booking.end_date

    def nights(self):
        return (self.end_date() - self.start_date()).days

    def total_price(self):
        return self.room.price * self.nights()

    def __str__(self):
        return "(%s %s) %s" % (self.booking_id, self.booking.owner, self.room.room_number)


class Privilege(models.Model):
    booking = models.ForeignKey(BookingDetail, related_name='booking_detail', on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    detail = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name='Used ?')

    type_choice = (
        (0, 'Wifi'),
        (1, 'Breakfast')
    )
    type = models.SmallIntegerField(null=True, choices=type_choice)

    class Meta:
        db_table = 'privilege'
