from django.core.validators import MaxValueValidator
from django.db import models


class BiomedicalEquipment(models.Model):
    monitor = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Monitor quantity",
    )
    aed = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="AED quantity",
    )
    adult_pads = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Adult pads quantity",
    )
    pediatric_pads = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric pads quantity",
    )
    aspirator = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Aspirator quantity",
    )
    flowmeter = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Flowmeter quantity",
    )
    glucometer = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Glucometer quantity",
    )
    pulse_oximeter = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Pulse oximeter quantity",
    )
    central_oxygen = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Central oxygen quantity",
    )
    portable_oxygen_1 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Portable oxygen #1 quantity",
    )
    portable_oxygen_2 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Portable oxygen #2 quantity",
    )
    spencer_scissors = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Spencer scissors quantity",
    )
    search_light = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Search light quantity",
    )
    reflex_hammer = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10)],
        help_text="Reflex hammer quantity",
    )

    def __str__(self):
        return f"BiomedicalEquipment #{self.pk}"
