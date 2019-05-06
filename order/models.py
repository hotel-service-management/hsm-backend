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
    booking_detail = models.ForeignKey(BookingDetail, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)
    total_price = models.FloatField(default=0)

    def total_price(self):
        return sum([i.price for i in self.service.all()])

    def __str__(self):
        return "Booking #%s %s - %s" % (
            self.booking_detail.booking_id, self.booking_detail.booking.owner, self.booking_detail.room.room_number)

    class Meta:
        db_table = 'orders'
