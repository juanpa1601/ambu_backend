from django.db import models

class PatientHistory(models.Model):
    
    has_pathology = models.BooleanField(default=False)
    pathology = models.TextField(
        blank=True,
        null=True
    )
    has_allergies = models.BooleanField(default=False)
    allergies = models.TextField(
        blank=True,
        null=True
    )
    has_surgies = models.BooleanField(default=False)
    surgeries = models.TextField(
        blank=True,
        null=True
    )
    has_medicines = models.BooleanField(default=False)
    medicines = models.TextField(
        blank=True,
        null=True
    )
    tobacco_use = models.BooleanField(default=False)
    alcohol_use = models.BooleanField(default=False)
    substance_use = models.BooleanField(default=False)
    substances = models.TextField(
        blank=True,
        null=True
    )
    other_history = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Patient History'
        verbose_name_plural = 'Patient Histories'