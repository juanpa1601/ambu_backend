from django.db import models
from .patient_history import PatientHistory
from .insurance_provider import InsuranceProvider
from core.models import (
    AuditedModel,
    ActiveManager
)

class Patient(AuditedModel):
    
    patient_name = models.CharField(max_length=200)
    identification_type = models.CharField(max_length=50)
    other_identification_type = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    identification_number = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )
    issue_date = models.DateField(
        null=True, 
        blank=True
    )
    issue_place = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    birth_date = models.DateField(
        null=True, 
        blank=True
    )
    age = models.IntegerField(
        null=True, 
        blank=True
    )
    sex = models.CharField(
        max_length=20,
        null=True, 
        blank=True
    )
    home_address = models.CharField(
        max_length=300,
        null=True,
        blank=True
    )
    residence_city = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    cell_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    landline_phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True
    )
    marital_status = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    occupation = models.CharField(
        max_length=100,
        blank=True, 
        null=True
    )
    signature = models.TextField(
        blank=True, 
        null=True
    )
    patient_history = models.OneToOneField(
        PatientHistory,
        on_delete=models.CASCADE,
        related_name='patient_history_patient',
        blank=True,
        null=True
    )
    insurance_provider = models.OneToOneField(
        InsuranceProvider,
        on_delete=models.CASCADE,
        related_name='insurance_provider_patient',
        blank=True,
        null=True
    )
    membership_category = models.CharField(
        max_length=50,
        blank=True,
        null=True    
    )

    # ✅ Manager personalizado
    objects = ActiveManager()  # Excluye eliminados por defecto
    all_objects = models.Manager()  # Incluye todos
    
    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']  # Heredado de AuditedModel
        indexes = [
            models.Index(fields=['identification_number']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self) -> str:
        return f'{self.patient_name} - {self.identification_number}'    