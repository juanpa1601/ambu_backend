from django.db import models

class Treatment(models.Model):

    monitors_vital_signs = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if vital signs were monitored'
    )
    oxygen = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if oxygen was administered'
    )
    liter_minute = models.FloatField(
        blank=True,
        null=True,
        help_text='Oxygen flow rate in liters per minute'
    )
    nasal_cannula = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if a nasal cannula was used'
    )
    simple_face_mask = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if a simple face mask was used'
    )
    non_rebreather_mask = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if a non-rebreather mask was used'
    )

    class Meta:
        verbose_name = 'Treatment'
        verbose_name_plural = 'Treatments'