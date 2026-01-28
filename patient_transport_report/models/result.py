from django.db import models

class Result(models.Model):

    no_vital_signs = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if no vital signs were recorded'
    )
    denies_transportation = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if the patient denies transportation'
    )
    schelud_transfer = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if a scheduled transfer was planned'
    )

    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'