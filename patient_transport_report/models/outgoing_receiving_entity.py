from django.db import models

class OutgoingReceivingEntity(models.Model):

    name = models.CharField(max_length=200)
    document = models.CharField(max_length=100)
    staff_title = models.CharField(max_length=100)
    signature = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Outgoing/Receiving Entity'
        verbose_name_plural = 'Outgoing/Receiving Entities'