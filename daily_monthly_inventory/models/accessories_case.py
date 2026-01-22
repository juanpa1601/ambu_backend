from django.db import models
from django.core.validators import MaxValueValidator


class AccessoriesCase(models.Model):
    adult_bp_cuff = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult BP cuff quantity",
    )
    pediatric_bp_cuff = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric BP cuff quantity",
    )
    adult_spo2_sensor = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult SPO2 sensor quantity",
    )
    pediatric_spo2_sensor = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric SPO2 sensor quantity",
    )
    carsioscope_cables = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Cardiac SPO2 sensor quantity",
    )
    temperature_sensor = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Temperature sensor quantity",
    )

    def __str__(self):
        return f"AccessoriesCase #{self.pk}"
