from django.db import models

class OutgoingReceivingEntity(models.Model):

    name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Name of the outgoing or receiving entity'
    )
    document = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Document identifier of the entity'    
    )
    staff_title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Title or position of the staff member representing the entity'
    )

    class Meta:
        verbose_name = 'Outgoing/Receiving Entity'
        verbose_name_plural = 'Outgoing/Receiving Entities'