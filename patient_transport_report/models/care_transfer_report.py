from django.db import models
from ...staff.models import (
    Driver,
    Healthcare
)
from ...daily_monthly_inventory.models import Ambulance
from .patient import Patient
from .companion import Companion
from .physical_exam import PhysicalExam
from .treatment import Treatment
from .diagnosis import Diagnosis
from .result import Result
from .complications_transfer import ComplicationsTransfer
from .outgoing_receiving_entity import OutgoingReceivingEntity

class CareTransferReport(models.Model):

    patient_one_of = models.IntegerField()
    transfer_type = models.CharField(max_length=50)
    initial_address = models.CharField(max_length=300)
    landmark = models.CharField(max_length=200)
    service_type = models.CharField(max_length=100)
    dispatch_time = models.DateTimeField()
    patient_arrival_time = models.DateTimeField()
    patient_departure_time = models.DateTimeField()
    arrival_time_patient = models.DateTimeField()
    double_departure_time = models.DateTimeField()
    double_arrival_time = models.DateTimeField()
    end_attention_time = models.DateTimeField()
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='driver_care_transfer_report'
    )
    attending_staff = models.ForeignKey(
        Healthcare,
        on_delete=models.CASCADE,
        related_name='attending_staff_care_transfer_report'
    )
    reg_number = models.CharField(max_length=100)
    support_staff = models.ForeignKey(
        Healthcare,
        on_delete=models.CASCADE,
        related_name='support_staff_care_transfer_report',
        blank=True,
        null=True
    )
    attending_staff_tittle = models.CharField(max_length=100)
    ambulance = models.ForeignKey(
        Ambulance,
        on_delete=models.CASCADE,
        related_name='ambulance_care_transfer_report'
    )
    patient = models.OneToOneField( # <----- TODO Verify if OneToOneField is correct here
        Patient,
        on_delete=models.CASCADE,
        related_name='patient_care_transfer_report'
    )
    companion_1 = models.ForeignKey(
        Companion,
        on_delete=models.CASCADE,
        related_name='companion_1_care_transfer_report',
        blank=True,
        null=True
    )
    companion_2 = models.ForeignKey(
        Companion,
        on_delete=models.CASCADE,
        related_name='companion_2_care_transfer_report',
        blank=True,
        null=True
    )
    initial_physicial_examination = models.OneToOneField(
        PhysicalExam,
        on_delete=models.CASCADE,
        related_name='initial_physical_exam_care_transfer_report'
    )
    skin_condition = models.CharField(max_length=100) # <------ TODO Multiples valores
    hemodynamic_status = models.CharField(max_length=100) # <------ TODO Multiples valores
    treatment = models.OneToOneField(
        Treatment,
        on_delete=models.CASCADE,
        related_name='treatment_care_transfer_report'
    )
    diagnosis_1 = models.ForeignKey(
        Diagnosis,
        on_delete=models.CASCADE,
        related_name='diagnosis_1_care_transfer_report'
    )
    diagnosis_2 = models.ForeignKey(
        Diagnosis,
        on_delete=models.CASCADE,
        related_name='diagnosis_2_care_transfer_report',
        blank=True,
        null=True
    )
    result = models.OneToOneField(
        Result,
        on_delete=models.CASCADE,
        related_name='result_care_transfer_report'
    )
    complications_transfer = models.OneToOneField(
        ComplicationsTransfer,
        on_delete=models.CASCADE,
        related_name='complications_transfer_care_transfer_report'
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    final_physical_examination = models.OneToOneField(
        PhysicalExam,
        on_delete=models.CASCADE,
        related_name='final_physical_exam_care_transfer_report'
    )
    receiving_entity = models.OneToOneField(
        OutgoingReceivingEntity,
        on_delete=models.CASCADE,
        related_name='receiving_entity_care_transfer_report'
    )

    class Meta:
        verbose_name = 'Care Transfer Report'
        verbose_name_plural = 'Care Transfer Reports'