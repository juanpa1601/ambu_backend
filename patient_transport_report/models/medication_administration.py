from django.db import models

class MedicationAdministration(models.Model):

    oxygen = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if oxygen was administered'
    )
    iv_fluids = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if IV fluids were administered'
    )
    admin_route_type = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates the type of administration route used'
    )
    other_medication_details = models.TextField(
        blank=True,
        null=True,
        help_text='Details of other medications administered'
    )

    class Meta:
        verbose_name = 'Medication Administration'
        verbose_name_plural = 'Medication Administrations'