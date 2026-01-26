from django.db import models

class RequiredProcedures(models.Model):

    immovilization = models.BooleanField(default=False)
    streatcher_transfer = models.BooleanField(default=False)
    ambulance_transport = models.BooleanField(default=False)
    assessment = models.BooleanField(default=False)
    other_procedures_details = models.TextField(
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = 'Required Procedure'
        verbose_name_plural = 'Required Procedures'