from django.db import models
from .required_procedures import RequiredProcedures
from .medication_administration import MedicationAdministration
from .companion import Companion
from ...staff.models import Healthcare
from .outgoing_receiving_entity import OutgoingReceivingEntity

class InformedConsent(models.Model):
    '''
    Informed consent form.
    Now connected through PatientTransportReport instead of direct Patient reference.
    '''

    consent_timestamp = models.DateTimeField(auto_now_add=True)
    guardian_type = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=200)
    responsible_for = models.CharField(max_length=200)
    guardian_id_type = models.CharField(max_length=50)
    guardian_id_number = models.CharField(max_length=100)
    required_procedures = models.OneToOneField(
        RequiredProcedures,
        on_delete=models.CASCADE,
        related_name='required_procedures_informed_consent'
    )
    administers_medications = models.BooleanField(default=False)
    medication_administration = models.OneToOneField(
        MedicationAdministration,
        on_delete=models.CASCADE,
        related_name='medication_administration_informed_consent',
        blank=True,
        null=True
    )
    service_type = models.CharField(max_length=100)
    other_implications = models.TextField(
        blank=True,
        null=True
    )
    patient_can_sign = models.BooleanField(default=True)
    responsible_can_sign = models.BooleanField(default=False)
    responsible = models.ForeignKey(
        Companion,
        on_delete=models.CASCADE,
        related_name='responsible_informed_consents',
        blank=True,
        null=True
    )
    attending_staff = models.ForeignKey(
        Healthcare,
        on_delete=models.CASCADE,
        related_name='attending_staff_informed_consent'
    )
    outgoing_entity = models.OneToOneField(
        OutgoingReceivingEntity,
        on_delete=models.CASCADE,
        related_name='outgoing_entity_informed_consent'
    )

    class Meta:
        verbose_name = 'Informed Consent'
        verbose_name_plural = 'Informed Consents'