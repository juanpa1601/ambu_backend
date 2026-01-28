from rest_framework import serializers
from patient_transport_report.models import Patient
from .patient_history_detail_serializer import PatientHistoryDetailSerializer
from .insurance_provider_detail_serializer import InsuranceProviderDetailSerializer
from datetime import date

class PatientDetailSerializer(serializers.ModelSerializer):
    '''Complete serializer for Patient with nested history and insurance.'''
    
    patient_age: int | None = serializers.SerializerMethodField()
    
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
    ) -> int | None:
        '''Calculate patient age from birth_date.'''
        if not obj.birth_date:
            return None
        today: date = date.today()
        age: int = today.year - obj.birth_date.year
        if (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day):
            age -= 1
        return age