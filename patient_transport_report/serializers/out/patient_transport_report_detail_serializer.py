from rest_framework import serializers
from patient_transport_report.models import PatientTransportReport
from .patient_detail_serializer import PatientDetailSerializer
from .informed_consent_detail_serializer import InformedConsentDetailSerializer
from .care_transfer_report_detail_serializer import CareTransferReportDetailSerializer
from .satisfaction_survey_detail_serializer import SatisfactionSurveyDetailSerializer

class PatientTransportReportDetailSerializer(serializers.ModelSerializer):
    '''Complete serializer for PatientTransportReport with all nested relationships.'''
    
    patient: PatientDetailSerializer = PatientDetailSerializer(read_only=True)
    informed_consent: InformedConsentDetailSerializer = InformedConsentDetailSerializer(read_only=True)
    care_transfer_report: CareTransferReportDetailSerializer = CareTransferReportDetailSerializer(read_only=True)
    satisfaction_survey: SatisfactionSurveyDetailSerializer = SatisfactionSurveyDetailSerializer(read_only=True)
    
    created_by_username: serializers.CharField = serializers.CharField(
        source='created_by.username', 
        read_only=True
    )
    updated_by_username: serializers.CharField = serializers.CharField(
        source='updated_by.username', 
        read_only=True
    )
    
    class Meta:
        model = PatientTransportReport
        fields = [
            'id',
            'patient',
            'informed_consent',
            'care_transfer_report',
            'satisfaction_survey',
            'status',
            'created_at',
            'updated_at',
            'created_by',
            'created_by_username',
            'updated_by',
            'updated_by_username'
        ]
        read_only_fields = fields