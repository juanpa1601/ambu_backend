from django.db import models

class ComplicationsTransfer(models.Model):

    description_complication = models.TextField(
        blank=True,
        null=True,
        help_text='Description of the complication that occurred during transfer'
    )
    register_code = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if a register code was recorded'
    )
    code = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text='Code associated with the complication'
    )
    record_waiting_time = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if waiting time was recorded'
    )
    waiting_time = models.DurationField( #HH:MM:SS <---- TODO
        blank=True,
        null=True,
        help_text='Waiting time duration'
    )
    time_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Time associated with the code'
    )

    class Meta:
        verbose_name = 'Complication Transfer'
        verbose_name_plural = 'Complications Transfer'