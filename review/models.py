from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(models.Model):
    score = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(0)
    ])
    title = models.CharField(max_length=100)
    description = models.TextField()

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return "(%s/%s) %s" % (self.booking.id, self.score, self.title)
