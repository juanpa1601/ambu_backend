from rest_framework import serializers
from patient_transport_report.models import Patient
from .patient_history_detail_serializer import PatientHistoryDetailSerializer
from .insurance_provider_detail_serializer import InsuranceProviderDetailSerializer
from datetime import date
from dateutil.relativedelta import relativedelta

class PatientDetailSerializer(serializers.ModelSerializer):
    '''Complete serializer for Patient with nested history and insurance.'''
    
    patient_age: str | None = serializers.SerializerMethodField()
    
    patient_history: PatientHistoryDetailSerializer = PatientHistoryDetailSerializer(read_only=True)
    insurance_provider: InsuranceProviderDetailSerializer = InsuranceProviderDetailSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'patient_name',
            'identification_type',
            'other_identification_type',
            'identification_number',
            'issue_date',
            'issue_place',
            'birth_date',
            'patient_age',
            'sex',
            'home_address',
            'residence_city',
            'cell_phone',
            'landline_phone',
            'marital_status',
            'occupation',
            'patient_history',
            'insurance_provider',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields
    
    def get_patient_age(
        self, 
        obj: Patient
    ) -> str | None:
        '''Calculate patient age with human-readable format.'''
        if not obj.birth_date:
            return None
        today: date = date.today()
        age_delta: relativedelta = relativedelta(
            today, 
            obj.birth_date
        )
        years: int = age_delta.years
        months: int = age_delta.months
        days: int = age_delta.days
        # Build human-readable string
        parts: list[str] = []
        if years > 0:
            parts.append(f"{years} año{'s' if years != 1 else ''}")
        if months > 0:
            parts.append(f"{months} mes{'es' if months != 1 else ''}")
        if days > 0:
            parts.append(f"{days} día{'s' if days != 1 else ''}")
        age_string: str = ", ".join(parts) if parts else "0 días"
        return age_string