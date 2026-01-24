from django.db import models
from .informed_consent import InformedConsent
from .satisfaction_survey import SatisfactionSurvey
from .care_transfer_report import CareTransferReport

class PatientTransportReport(models.Model):
    
    informed_consent = models.OneToOneField(
        InformedConsent,
        on_delete=models.CASCADE,
        related_name='patient_informed_consent'
    )
    care_transfer_report = models.OneToOneField(
        CareTransferReport,
        on_delete=models.CASCADE,
        related_name='patient_care_transfer_report'
    )
    satisfaction_survey = models.OneToOneField(
        SatisfactionSurvey,
        on_delete=models.CASCADE,
        related_name='patient_satisfaction_survey',
        blank=True,
        null=True
    )
    status = models.CharField(max_length=50)


    class Meta:
        verbose_name = 'Patient Transport Report'
        verbose_name_plural = 'Patient Transport Reports'

