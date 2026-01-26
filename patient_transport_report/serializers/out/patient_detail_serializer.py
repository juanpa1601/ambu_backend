from rest_framework import serializers
from patient_transport_report.models import Patient

class PatientDetailSerializer(serializers.ModelSerializer):
    '''Serializer for Patient details in report view.'''
    
    insurance_provider_name: serializers.CharField = serializers.CharField(
        source='insurance_provider.name', 
        read_only=True
    )
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'patient_name',
            'identification_type',
            'identification_number',
            'age',
            'sex',
            'phone',
            'insurance_provider',
            'insurance_provider_name',
            'affiliate_type',
            'address'
        ]
        read_only_fields = fields