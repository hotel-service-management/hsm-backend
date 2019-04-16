from django.db import models

from users.models import User


class Booking(models.Model):
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    num_person = models.IntegerField(null=False, default=1)
    stay_date = models.IntegerField(null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
