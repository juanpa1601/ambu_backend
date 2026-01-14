from django.db import models
from django.conf import settings

class BaseStaff(models.Model):

    system_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    document_type = models.CharField(
        max_length=50
    )
    document_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )
    type_personnel = models.CharField(
        max_length=50
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    birth_date = models.DateField(
        blank=True,
        null=True
    )
    signature = models.ImageField(
        upload_to='signatures/',
        blank=True,
        null=True,
        help_text='Digital signature of the healthcare staff'
    )

    class Meta:
        verbose_name = 'Base Staff'
        verbose_name_plural = 'Base Staffs'
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.system_user.get_full_name()} - {self.document_number}"
    