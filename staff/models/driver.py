from .base_staff import BaseStaff
from django.db import models

class Driver(models.Model):
    base_staff = models.OneToOneField(
        BaseStaff,
        on_delete=models.CASCADE,
        related_name='driver_profile',
        primary_key=True
    )
    license_number = models.CharField(
        max_length=50,
        unique=True,
        help_text='Driver license number'
    )
    license_category = models.CharField(
        max_length=20,
        help_text='Category of the driver license'
    )
    license_expiry_date = models.DateField(help_text='Expiry date of the driver license')
    license_issue_date = models.DateField(help_text='Issue date of the driver license')
    blood_type = models.CharField(
        max_length=5,
        help_text='Blood type of the driver'
    )

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
        ordering = ['-base_staff__created_at']