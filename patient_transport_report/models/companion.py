from django.db import models

class Companion(models.Model):

    name = models.CharField(max_length=200)
    identification_type = models.CharField(max_length=50)
    identification_number = models.CharField(max_length=100)
    kindship = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(
        max_length=254,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Companion'
        verbose_name_plural = 'Companions'