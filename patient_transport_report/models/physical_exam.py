from django.db import models
from .glasgow import Glasgow

class PhysicalExam(models.Model):

    systolic = models.FloatField(
        null=True,
        blank=True,
        help_text='Systolic blood pressure value'
    )
    diastolic = models.FloatField(
        null=True,
        blank=True,
        help_text='Diastolic blood pressure value'
    )
    map_pam = models.FloatField(
        null=True,
        blank=True,
        help_text='Mean arterial pressure (PAM) value'
    )
    heart_rate = models.FloatField(
        null=True,
        blank=True,
        help_text='Heart rate value'
    )
    respiratory_rate = models.FloatField(
        null=True,
        blank=True,
        help_text='Respiratory rate value'
    )
    oxygen_saturation = models.FloatField(
        null=True,
        blank=True,
        help_text='Oxygen saturation percentage'
    )
    temperature = models.FloatField(
        null=True,
        blank=True,
        help_text='Body temperature value'
    )
    blood_glucose = models.FloatField(
        null=True,
        blank=True,
        help_text='Blood glucose level'
    )
    glasgow = models.OneToOneField(
        Glasgow,
        on_delete=models.CASCADE,
        related_name='physical_exam_glasgow',
        null=True,
        blank=True,
        help_text='Glasgow Coma Scale assessment'
    )

    class Meta:
        verbose_name = 'Physical Exam'
        verbose_name_plural = 'Physical Exams'