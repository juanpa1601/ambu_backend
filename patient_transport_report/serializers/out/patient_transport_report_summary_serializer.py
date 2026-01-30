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
    created_by_full_name: serializers.CharField = serializers.SerializerMethodField()
    class Meta:
        model = PatientTransportReport
        fields = [
            'id',
            'patient_name',
            'patient_identification',
            'status',
            'created_at',
            'updated_at',
            'created_by_full_name'
        ]
        read_only_fields = fields

    def get_created_by_full_name(self, obj):
        user = obj.created_by
        return user.get_full_name() if user else ""