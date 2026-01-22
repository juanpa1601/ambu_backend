from django.db import models
from django.core.validators import MaxValueValidator


class ImmobilizationAndSafety(models.Model):
    adult_cervical_collar = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult cervical collar quantity",
    )
    pediatric_cervical_collar = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric cervical collar quantity",
    )
    adult_immobilization_kit = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult immobilization kit quantity",
    )
    pediatric_immobilization_kit = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric immobilization kit quantity",
    )
    benziral_spill_kit = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Benziral spill kit quantity",
    )
    west_solidifier_spill_kit = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="West solidifier spill kit quantity",
    )
    stretcher_side_rails = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Stretcher side rails quantity",
    )
    stretcher_harness_straps = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Stretcher harness straps quantity",
    )
    ambumedic_umbrella = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Ambumedic umbrella quantity",
    )
    safety_vests = models.IntegerField(
        default=0, validators=[MaxValueValidator(10)], help_text="Safety vests quantity"
    )

    def __str__(self):
        return f"ImmobilizationAndSafety #{self.pk}"
