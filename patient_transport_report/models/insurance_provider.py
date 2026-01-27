from django.db import models

class InsuranceProvider(models.Model):

    coverage_type = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=200)
    other_coverage_type = models.BooleanField(default=False)
    other_coverage_details = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Insurance Provider'
        verbose_name_plural = 'Insurance Providers'