from django.db import models

class InsuranceProvider(models.Model):

    coverage_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Type of insurance coverage'
    )
    provider_name = models.CharField(
        max_length=200,
        help_text='Name of the insurance provider',
        blank=True,
        null=True
    )
    other_coverage_type = models.BooleanField(
        blank=True,
        null=True
    )
    other_coverage_details = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Insurance Provider'
        verbose_name_plural = 'Insurance Providers'