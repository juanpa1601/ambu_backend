from django.db import models

class Glasgow(models.Model):

    motor = models.IntegerField(
        null=True,
        blank=True,
        help_text='Motor response score'
    )
    motor_text = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Description of motor response'
    )
    verbal = models.IntegerField(
        null=True,
        blank=True,
        help_text='Verbal response score'
    )
    verbal_text = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Description of verbal response'    
    )
    eyes_opening = models.IntegerField(
        null=True,
        blank=True,
        help_text='Eye opening response score'
    )
    eyes_opening_text = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Description of eye opening response'
    )
    total = models.IntegerField(
        null=True,
        blank=True,
        help_text='Total Glasgow Coma Scale score'
    )

    class Meta:
        verbose_name = 'Glasgow'
        verbose_name_plural = 'Glasgows'