from django.db import models
from django.core.validators import MaxValueValidator


class BiomedicalEquipment(models.Model):
    monitor = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Monitor quantity"
    )
    aed = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="AED quantity"
    )
    adult_pads = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult pads quantity"
    )
    pediatric_pads = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric pads quantity"
    )
    aspirator = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Aspirator quantity"
    )
    flowmeter = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Flowmeter quantity"
    )
    glucometer = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Glucometer quantity"
    )
    pulse_oximeter = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pulse oximeter quantity"
    )
    central_oxygen = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Central oxygen quantity"
    )
    portable_oxygen_1 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Portable oxygen #1 quantity"
    )
    portable_oxygen_2 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Portable oxygen #2 quantity"
    )
    spencer_scissors = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Spencer scissors quantity"
    )
    search_light = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Search light quantity"
    )
    reflex_hammer = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Reflex hammer quantity"
    )

    def __str__(self):
        return f"BiomedicalEquipment #{self.pk}"
