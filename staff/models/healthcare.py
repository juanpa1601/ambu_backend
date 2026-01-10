from .base_staff import BaseStaff
from django.db import models

class Healthcare(models.Model):
    base_staff = models.OneToOneField(
        BaseStaff,
        on_delete=models.CASCADE,
        related_name='healthcare_profile',
        primary_key=True
    )
    professional_registration = models.CharField(
        max_length=50,
        unique=True,
        help_text='Professional registration number'
    )
    professional_position = models.CharField(
        max_length=50,
        help_text='Position held by the healthcare staff'
    )
    signature = models.ImageField(
        upload_to='signatures/',
        blank=True,
        null=True,
        help_text='Digital signature of the healthcare staff'
    )

    class Meta:
        verbose_name = 'Healthcare Staff'
        verbose_name_plural = 'Healthcare Staffs'
        ordering = ['-base_staff__created_at']
