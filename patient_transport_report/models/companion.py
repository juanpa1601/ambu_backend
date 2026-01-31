from django.db import models

class Companion(models.Model):

    name = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        help_text='Full name of the companion'
    )
    identification_number = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        db_index=True,
        help_text='Identification document number'
    )
    kindship = models.CharField(
        null=True,
        blank=True,        
        max_length=100,
        help_text='Relationship to the patient'
    )
    phone_number = models.CharField(
        null=True,
        blank=True,        
        max_length=20,
        help_text='Contact phone number'
    )

    class Meta:
        verbose_name = 'Companion'
        verbose_name_plural = 'Companions'