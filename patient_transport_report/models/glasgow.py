from django.db import models

class Glasgow(models.Model):

    motor = models.IntegerField()
    motor_text = models.CharField(max_length=100)
    verbal = models.IntegerField()
    verbal_text = models.CharField(max_length=100)
    eyes_opening = models.IntegerField()
    eyes_opening_text = models.CharField(max_length=100)
    total = models.IntegerField()

    class Meta:
        verbose_name = 'Glasgow'
        verbose_name_plural = 'Glasgows'