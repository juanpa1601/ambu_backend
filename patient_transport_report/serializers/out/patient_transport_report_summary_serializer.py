from rest_framework import serializers
from patient_transport_report.models import PatientTransportReport

class PatientTransportReportSummarySerializer(serializers.ModelSerializer):
    '''
    Serializer for PatientTransportReport summary (for inbox/buzon listing).
    
    Returns minimal information for list views.
    '''
    
    patient_name: serializers.CharField = serializers.CharField(
        source='patient.patient_name', 
        read_only=True
    )
    patient_identification: serializers.CharField = serializers.CharField(
        source='patient.identification_number', 
        read_only=True
    )
    created_by_username: serializers.CharField = serializers.CharField(
        source='created_by.username', 
        read_only=True
    )
    
    class Meta:
        model = PatientTransportReport
        fields = [
            'id',
            'patient_name',
            'patient_identification',
            'status',
            'created_at',
            'updated_at',
            'created_by_username'
        ]
        read_only_fields = fields