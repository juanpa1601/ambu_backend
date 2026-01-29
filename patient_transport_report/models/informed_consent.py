from django.db import models
from .required_procedures import RequiredProcedures
from .medication_administration import MedicationAdministration
from .outgoing_receiving_entity import OutgoingReceivingEntity
from core.models import (
    AuditedModel, 
    ActiveManager
)

class InformedConsent(AuditedModel):
    '''
    Informed consent form.
    Now connected through PatientTransportReport instead of direct Patient reference.
    '''

    consent_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when consent was given'
    )
    guardian_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Type of guardian (e.g., parent, legal representative)'
    )
    guardian_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Name of the guardian or responsible person'
    )
    responsible_for = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Name of the person the guardian is responsible for'
    )
    guardian_id_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Type of identification for the guardian (e.g., ID card, passport)'
    )
    guardian_id_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Identification number of the guardian'
    )
    required_procedures = models.OneToOneField(
        RequiredProcedures,
        on_delete=models.CASCADE,
        related_name='required_procedures_informed_consent',
        blank=True,
        null=True,
        help_text='Procedures that require consent'
    )
    administers_medications = models.BooleanField(
        null=True,
        blank=True,        
        help_text='Indicates if medication administration is consented'
    )
    medication_administration = models.OneToOneField(
        MedicationAdministration,
        on_delete=models.CASCADE,
        related_name='medication_administration_informed_consent',
        blank=True,
        null=True,
        help_text='Details about medication administration'
    )
    service_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Type of service provided'
    )
    other_implications = models.TextField(
        blank=True,
        null=True,
        help_text='Other implications explained to the patient/guardian'
    )
    patient_can_sign = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if the patient is able to sign the consent'
    )
    patient_signature = models.TextField(
        blank=True,
        null=True,
        help_text='Digital signature in base64 format'
    )
    responsible_can_sign = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if the responsible guardian can sign the consent'
    )
    responsible_signature = models.TextField(
        blank=True,
        null=True,
        help_text='Digital signature in base64 format'
    )
    attending_staff_signature = models.TextField(
        blank=True,
        null=True,
        help_text='Digital signature in base64 format'
    )
    outgoing_entity = models.ForeignKey(
        OutgoingReceivingEntity,
        on_delete=models.CASCADE,
        related_name='outgoing_entity_informed_consents',
        blank=True,
        null=True,
        help_text='Entity receiving the informed consent'
    )
    outgoing_entity_signature = models.TextField(
        blank=True,
        null=True,
        help_text='Digital signature in base64 format'
    )

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = 'Informed Consent'
        verbose_name_plural = 'Informed Consents'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Informed Consent #{self.id} - Guardian: {self.guardian_name}'