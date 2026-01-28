from __future__ import annotations
from django.db import models
from staff.models import (
    Driver, 
    Healthcare
)
from daily_monthly_inventory.models import Ambulance
from .patient import Patient
from .companion import Companion
from .physical_exam import PhysicalExam
from .treatment import Treatment
from .diagnosis import Diagnosis
from .result import Result
from .complications_transfer import ComplicationsTransfer
from .outgoing_receiving_entity import OutgoingReceivingEntity
from .skin_condition import SkinCondition
from .hemodynamic_status import HemodynamicStatus
from core.models import (
    AuditedModel, 
    ActiveManager
)
from .ips import IPS

class CareTransferReport(AuditedModel):
    '''
    Report of patient care and transfer.
    Connected to patient through PatientTransportReport.
    '''
    
    patient_one_of = models.IntegerField(
        null=True,
        blank=True,
        help_text='Unique identifier for the patient within the care transfer report'
    )
    transfer_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='Type of transfer (e.g., emergency, non-emergency)'    
    )
    initial_address = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text='Initial address of the patient'
    )
    landmark = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Landmark near the initial address'
    )
    service_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Type of service provided'
    )
    
    # Timestamps
    dispatch_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the ambulance was dispatched'
    )
    patient_arrival_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the ambulance arrived at the patient location'
    )
    patient_departure_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the ambulance departed from the patient location'
    )
    arrival_time_patient = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the ambulance arrived at the destination with the patient'
    )
    double_departure_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the ambulance departed from the destination'
    )
    double_arrival_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the ambulance arrived back at the base'
    )
    end_attention_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the care attention ended'
    )
    
    # Staff relationships
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='driver_care_transfer_reports',
        null=True,
        blank=True,
        help_text='Driver of the ambulance'
    )
    attending_staff = models.ForeignKey(
        Healthcare,
        on_delete=models.CASCADE,
        related_name='attending_staff_care_transfer_reports',
        help_text='Healthcare staff attending the patient'
    )
    reg_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Registration number of the attending staff'    
    )
    support_staff = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Support healthcare staff attending the patient'
    )
    attending_staff_title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Title of the attending staff'
    )
    
    # Ambulance
    ambulance = models.ForeignKey(
        Ambulance,
        on_delete=models.CASCADE,
        related_name='ambulance_care_transfer_reports',
        null=True,
        blank=True,
        help_text='Ambulance used for the transport'
    )
    
    # Companions
    companion = models.ForeignKey(
        Companion,
        on_delete=models.SET_NULL,
        related_name='companion_care_transfer_reports',
        blank=True,
        null=True,
        help_text='Companion accompanying the patient'
    )
    companion_is_responsible = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if the companion is the responsible guardian'    
    )
    responsible = models.ForeignKey(
        Companion,
        on_delete=models.SET_NULL,
        related_name='responsible_care_transfer_reports',
        blank=True,
        null=True,
        help_text='Responsible companion'
    )
    
    # Physical examinations
    initial_physical_exam = models.OneToOneField(
        PhysicalExam,
        on_delete=models.CASCADE,
        related_name='initial_physical_exam_care_transfer_report',
        null=True,
        blank=True,
        help_text='Initial physical examination of the patient'
    )
    final_physical_exam = models.OneToOneField(
        PhysicalExam,
        on_delete=models.CASCADE,
        related_name='final_physical_exam_care_transfer_report',
        null=True,
        blank=True,
        help_text='Final physical examination of the patient'
    )
    
    # Status fields - ManyToMany
    skin_conditions = models.ManyToManyField(
        SkinCondition,
        related_name='care_transfer_reports',
        blank=True,
        help_text='Select 1 or 2 skin conditions'
    )
    hemodynamic_statuses = models.ManyToManyField(
        HemodynamicStatus,
        related_name='care_transfer_reports',
        blank=True,
        help_text='Select 1 or 2 hemodynamic statuses'
    )
    
    # Medical information
    treatment = models.OneToOneField(
        Treatment,
        on_delete=models.CASCADE,
        related_name='treatment_care_transfer_report',
        null=True,
        blank=True,
        help_text='Treatment provided during the transport'
    )
    diagnosis_1 = models.ForeignKey(
        Diagnosis,
        on_delete=models.CASCADE,
        related_name='diagnosis_1_care_transfer_reports',
        blank=True,
        null=True,
        help_text='Primary diagnosis of the patient'
    )
    diagnosis_2 = models.ForeignKey(
        Diagnosis,
        on_delete=models.CASCADE,
        related_name='diagnosis_2_care_transfer_reports',
        blank=True,
        null=True,
        help_text='Secondary diagnosis of the patient'
    )
    result = models.OneToOneField(
        Result,
        on_delete=models.CASCADE,
        related_name='result_care_transfer_report',
        null=True,
        blank=True,
        help_text='Results obtained during the transport'
    )
    ips = models.ForeignKey(
        IPS,
        on_delete=models.CASCADE,
        related_name='ips_care_transfer_reports',
        null=True,
        blank=True,
        help_text='IPS associated with the care transfer report'
    )
    complications_transfer = models.OneToOneField(
        ComplicationsTransfer,
        on_delete=models.CASCADE,
        related_name='complications_transfer_care_transfer_report',
        null=True,
        blank=True,
        help_text='Complications that occurred during the transfer'
    )
    
    # Additional information
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Additional notes regarding the care transfer'
    )
    receiving_entity = models.ForeignKey(
        OutgoingReceivingEntity,
        on_delete=models.CASCADE,
        related_name='receiving_entity_care_transfer_report',
        blank=True,
        null=True,
        help_text='Entity receiving the patient'
    )
    receiving_entity_signature = models.TextField(
        blank=True,
        null=True,
        help_text='Digital signature in base64 format'
    )
    
    objects = ActiveManager()
    all_objects = models.Manager()
    
    class Meta:
        verbose_name = 'Care Transfer Report'
        verbose_name_plural = 'Care Transfer Reports'
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f'Care Transfer Report #{self.id} ({self.dispatch_time})'
    
    @property
    def patient(self) -> Patient | None:
        '''Access patient through PatientTransportReport'''
        return self.transport_report.patient if hasattr(self, 'transport_report') else None