from django.db import models

from booking.models import BookingDetail


class Service(models.Model):
    type_choices = (
        ('01', 'Food'),
        ('02', 'Service')
    )
    type = models.CharField(max_length=255, default='01', choices=type_choices, null=True)
    title = models.CharField(max_length=255, null=True)
    detail = models.TextField(null=True)
    price = models.FloatField()

    def __str__(self):
        return "%s - %s (%s)" % (self.get_type_display(), self.title, self.price)

    class Meta:
        db_table = 'services'


class Order(models.Model):
    booking = models.ForeignKey(BookingDetail, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)

    def __str__(self):
        return "Booking #%s %s - %s" % (self.booking.booking_id, self.booking.booking.owner, self.booking.room.room_number)

    class Meta:
        db_table = 'orders'
