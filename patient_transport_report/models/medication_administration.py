from django.db import models

class MedicationAdministration(models.Model):

    oxygen = models.BooleanField(default=False)
    iv_fluids = models.BooleanField(default=False)
    admin_route_type = models.BooleanField(default=False)
    other_medication_details = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Medication Administration'
        verbose_name_plural = 'Medication Administrations'