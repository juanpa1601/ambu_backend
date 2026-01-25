from django.db import models
from .informed_consent import InformedConsent
from .satisfaction_survey import SatisfactionSurvey
from .care_transfer_report import CareTransferReport
from .patient import Patient

class PatientTransportReport(models.Model):
    '''
    Main report entity that aggregates all patient-related data.
    When a patient is deleted, all their reports must be deleted.
    '''
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='transport_reports',
        help_text='Patient associated with this transport report'
    )
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
    status = models.CharField(
        max_length=50,
        choices=[
            ('borrador', 'Borrador'),
            ('completado', 'Completado'),
        ],
        default='borrador'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Patient Transport Report'
        verbose_name_plural = 'Patient Transport Reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self) -> str:
        return f'Report #{self.id} - Patient: {self.patient} ({self.status})'

