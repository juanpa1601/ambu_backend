from django.db import models

class PatientHistory(models.Model):
    
    has_pathology = models.BooleanField(
        blank=True,
        null=True        
    )
    pathology = models.TextField(
        blank=True,
        null=True
    )
    has_allergies = models.BooleanField(
        blank=True,
        null=True
    )
    allergies = models.TextField(
        blank=True,
        null=True
    )
    has_surgies = models.BooleanField(
        blank=True,
        null=True
    )
    surgeries = models.TextField(
        blank=True,
        null=True
    )
    has_medicines = models.BooleanField(
        blank=True,
        null=True
    )
    medicines = models.TextField(
        blank=True,
        null=True
    )
    tobacco_use = models.BooleanField(
        blank=True,
        null=True
    )
    alcohol_use = models.BooleanField(
        blank=True,
        null=True
    )
    substance_use = models.BooleanField(
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