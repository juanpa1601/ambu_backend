from django.db import models
from .patient_history import PatientHistory
from .insurance_provider import InsuranceProvider

class Patient(models.Model):
    
    patient_name = models.CharField(max_length=200)
    identification_type = models.CharField(max_length=50)
    other_identification_type = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    identification_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    issue_place = models.CharField(max_length=200)
    birth_date = models.DateField()
    age = models.IntegerField()
    sex = models.CharField(max_length=20)
    home_address = models.CharField(max_length=300)
    residence_city = models.CharField(max_length=100)
    cell_phone = models.CharField(max_length=20)
    landline_phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True
    )
    marital_status = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100)
    signature = models.TextField(
        blank=True, 
        null=True
    )
    patient_history = models.OneToOneField(
        PatientHistory,
        on_delete=models.CASCADE,
        related_name='patient_history_patient'
    )
    insurance_provider = models.OneToOneField(
        InsuranceProvider,
        on_delete=models.CASCADE,
        related_name='insurance_provider_patient'
    )
    membership_category = models.CharField(max_length=50)