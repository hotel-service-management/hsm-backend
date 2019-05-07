from django.db import models

from review.models import Review
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
    review = models.OneToOneField(Review, on_delete=models.CASCADE, null=True, blank=True)

    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'bookings'

    def nights(self):
        return (self.end_date - self.start_date).days

    def total_price(self):
        return sum([i.room.price * self.nights() for i in BookingDetail.objects.all().filter(booking=self.id)])

    def __str__(self):
        return "(%s) %s" % (self.id, self.owner)


class RoomType(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'room_type'


class Room(models.Model):
    price = models.FloatField(default=0)
    floor = models.IntegerField(default=1)
    room_number = models.CharField(max_length=10, blank=True, null=True)

    type = models.ForeignKey(RoomType, related_name='room_type', null=True, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        return "(%s) %s" % (self.room_number, self.type)


class BookingDetail(models.Model):
    class Meta:
        db_table = 'booking_detail'
        verbose_name = 'Booking Detail'
        verbose_name_plural = 'Booking Details'

    booking = models.ForeignKey(Booking, related_name='detail', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)

    def start_date(self):
        return self.booking.start_date

    def end_date(self):
        return self.booking.end_date

    def nights(self):
        return (self.end_date() - self.start_date()).days

    def get_total_price(self):
        return self.room.price * self.nights()

    def __str__(self):
        return "(%s %s) %s" % (self.booking_id, self.booking.owner, self.room.room_number)


class PrivilegeType(models.Model):
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'privilege_type'


class Privilege(models.Model):
    booking = models.ForeignKey(BookingDetail, related_name='booking_detail', on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    detail = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name='Used')

    type = models.ForeignKey(PrivilegeType, related_name='privilege_type', null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'privilege'
