from django.db import models

from booking.models import BookingDetail


class Order(models.Model):
    booking = models.ForeignKey(BookingDetail, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'


class Service(models.Model):
    type_choices = (
        ('01', 'food'),
        ('02', 'service')
    )
    type = models.CharField(max_length=255, default='01', choices=type_choices, null=True)
    price = models.FloatField()

    class Meta:
        db_table = 'services'


class ServiceList(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)

    class Meta:
        db_table = 'service_list'
