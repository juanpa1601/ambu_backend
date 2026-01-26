from django.db import models
from .glasgow import Glasgow

class PhysicalExam(models.Model):

    systolic = models.FloatField()
    diastolic = models.FloatField()
    map_pam = models.FloatField()
    heart_rate = models.FloatField()
    respiratory_rate = models.FloatField()
    oxygen_saturation = models.FloatField()
    temperature = models.FloatField()
    blood_glucose = models.FloatField()
    glasgow = models.OneToOneField(
        Glasgow,
        on_delete=models.CASCADE,
        related_name='physical_exam_glasgow'
    )

    class Meta:
        verbose_name = 'Physical Exam'
        verbose_name_plural = 'Physical Exams'