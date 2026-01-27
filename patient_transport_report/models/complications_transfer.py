from django.db import models

class ComplicationsTransfer(models.Model):

    description_complication = models.TextField()
    register_code = models.BooleanField(default=False)
    code = models.CharField(
        max_length=50, 
        blank=True, 
        null=True
    )
    record_waiting_time = models.BooleanField(default=False)
    waiting_time = models.DurationField( #HH:MM:SS <---- TODO
        blank=True,
        null=True
    )
    time_code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Complication Transfer'
        verbose_name_plural = 'Complications Transfer'