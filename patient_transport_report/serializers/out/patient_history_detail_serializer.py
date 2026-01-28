from rest_framework import serializers
from patient_transport_report.models import PatientHistory

class PatientHistoryDetailSerializer(serializers.ModelSerializer):
    '''Serializer for patient medical history.'''
    
    class Meta:
        model = PatientHistory
        fields = [
            'id',
            'has_pathology',
            'pathology',
            'has_allergies',
            'allergies',
            'has_surgeries',
            'surgeries',
            'has_medicines',
            'medicines',
            'tobacco_use',
            'substance_use',
            'alcohol_use',
            'other_history'
        ]
        read_only_fields = fields