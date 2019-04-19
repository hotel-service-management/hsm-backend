from django.db import models

from booking.models import BookingDetail


class Order(models.Model):
    booking = models.ForeignKey(BookingDetail, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order'


class Service(models.Model):
    type = models.CharField(max_length=255)
    price = models.FloatField()

    class Meta:
        db_table = 'service'


class ServiceList(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)

    class Meta:
        db_table = 'service_list'


class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()

    class Meta:
        db_table = 'food'


class FoodList(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ManyToManyField(Food)

    class Meta:
        db_table = 'food_list'
