from django.db import models
from django.core.validators import MaxValueValidator


class Surgical(models.Model):
    surgical_soap = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Surgical soap quantity",
    )
    antiseptic_soap = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Antiseptic soap quantity",
    )
    alcohol_120ml = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Alcohol 120ml quantity",
    )
    safety_goggles = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Safety goggles quantity",
    )
    kidney_dish = models.IntegerField(
        default=0, validators=[MaxValueValidator(10)], help_text="Kidney dish quantity"
    )
    magill_forceps = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Magill forceps quantity",
    )
    thermal_blanket = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Thermal blanket quantity",
    )
    triangular_bandage = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Triangular bandage quantity",
    )
    sterile_surgical_gauze = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Sterile surgical gauze quantity",
    )
    gauze_compress = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Gauze compress quantity",
    )
    elastic_bandage = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Elastic bandage quantity",
    )
    gauze_bandage = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Gauze bandage quantity",
    )
    cotton_bundle = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Cotton bundle quantity",
    )
    sterile_gloves = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Sterile gloves quantity",
    )

    def __str__(self):
        return f"Surgical #{self.pk}"
