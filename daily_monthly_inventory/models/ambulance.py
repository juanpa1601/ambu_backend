from django.core.validators import MaxValueValidator
from django.db import models


class Ambulance(models.Model):
    mobile_number = models.IntegerField(
        default=0, validators=[MaxValueValidator(10)], help_text="Mobile number"
    )
    license_plate = models.TextField(
        default="", blank=True, help_text="Observations and comments"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Ambulance #{self.pk}"
