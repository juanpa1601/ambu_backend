from django.db import models

class Treatment(models.Model):

    monitors_vital_signs = models.BooleanField(default=False)
    oxygen = models.BooleanField(default=False)
    liter_minute = models.FloatField(
        blank=True,
        null=True
    )
    nasal_cannula = models.BooleanField(default=False)
    simple_face_mask = models.BooleanField(default=False)
    non_rebreather_mask = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Treatment'
        verbose_name_plural = 'Treatments'