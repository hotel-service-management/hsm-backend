from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    gender_choices = ((1, 'Male'), (2, 'Female'))
    gender = models.SmallIntegerField(choices=gender_choices, default=1)
    address = models.TextField(null=False)
