from django.db import models

class Result(models.Model):

    no_vital_signs = models.BooleanField(default=False)
    denies_transportation = models.BooleanField(default=False)
    schelud_transfer = models.BooleanField(default=False)
    receiving_institution = models.TextField(
        blank=True,
        null=True
    )


    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'