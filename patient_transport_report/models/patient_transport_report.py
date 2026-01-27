from django.db import models
from .informed_consent import InformedConsent
from .satisfaction_survey import SatisfactionSurvey
from .care_transfer_report import CareTransferReport
from .patient import Patient
from core.models import (
    AuditedModel,
    ActiveManager
)
from django.contrib.auth.models import User

class PatientTransportReport(AuditedModel):
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
        default='borrador',
        db_index=True
    )

    objects = ActiveManager()
    all_objects = models.Manager()
    
    class Meta:
        verbose_name = 'Patient Transport Report'
        verbose_name_plural = 'Patient Transport Reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['created_by']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self) -> str:
        return f'Report #{self.id} - {self.patient.patient_name} ({self.status})'
    
    def complete(
        self, 
        user: User
    ) -> None:
        '''Mark report as completed with audit trail'''
        self.status = 'completado'
        self.updated_by = user
        self.save(update_fields=['status', 'updated_by', 'updated_at'])

