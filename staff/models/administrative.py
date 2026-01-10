from .base_staff import BaseStaff
from django.db import models

class Administrative(models.Model):
    base_staff = models.OneToOneField(
        BaseStaff,
        on_delete=models.CASCADE,
        related_name='administrative_profile',
        primary_key=True
    )
    department = models.CharField(
        max_length=100,
        help_text='Department where the administrative staff works'
    )
    role = models.CharField(
        max_length=100,
        help_text='Role of the administrative staff'
    )
    access_level = models.CharField(
        max_length=50,
        help_text='Access level of the administrative staff'
    )
    signature = models.ImageField(
        upload_to='signatures/',
        blank=True,
        null=True,
        help_text='Digital signature of the administrative staff'
    )

    class Meta:
        verbose_name = 'Administrative Staff'
        verbose_name_plural = 'Administrative Staffs'
        ordering = ['-base_staff__created_at']