from django.db import models

class RequiredProcedures(models.Model):

    immovilization = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if immovilization was required'
    )
    streatcher_transfer = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if stretcher transfer was required'
    )
    ambulance_transport = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if ambulance transport was required'
    )
    assessment = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if patient assessment was required'
    )
    other_procedures_details = models.TextField(
        blank=True, 
        null=True,
        help_text='Details of other required procedures'
    )

    class Meta:
        verbose_name = 'Required Procedure'
        verbose_name_plural = 'Required Procedures'