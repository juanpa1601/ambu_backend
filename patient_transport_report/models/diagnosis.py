from django.db import models

class Diagnosis(models.Model):

    cie_10 = models.CharField(max_length=10)
    cie_10_name = models.TextField()

    class Meta:
        verbose_name = 'Diagnosis'
        verbose_name_plural = 'Diagnoses'