from rest_framework import serializers
from patient_transport_report.models import PatientTransportReport
from .patient_detail_serializer import PatientDetailSerializer
from .informed_consent_detail_serializer import InformedConsentDetailSerializer
from .care_transfer_report_detail_serializer import CareTransferReportDetailSerializer
from .satisfaction_survey_detail_serializer import SatisfactionSurveyDetailSerializer
from .healthcare_staff_detail_serializer import HealthcareStaffDetailSerializer

class PatientTransportReportDetailSerializer(serializers.ModelSerializer):
    '''Complete serializer for PatientTransportReport with all nested relationships.'''
    
    attending_staff: HealthcareStaffDetailSerializer = HealthcareStaffDetailSerializer(read_only=True)
    patient: PatientDetailSerializer = PatientDetailSerializer(read_only=True)
    informed_consent: InformedConsentDetailSerializer = InformedConsentDetailSerializer(read_only=True)
    care_transfer_report: CareTransferReportDetailSerializer = CareTransferReportDetailSerializer(read_only=True)
    satisfaction_survey: SatisfactionSurveyDetailSerializer = SatisfactionSurveyDetailSerializer(read_only=True)
    
    created_by_username: serializers.CharField = serializers.CharField(
        source='created_by.username', 
        read_only=True,
        allow_null=True
    )
    created_by_full_name: serializers.SerializerMethodField = serializers.SerializerMethodField()
    
    updated_by_username: serializers.CharField = serializers.CharField(
        source='updated_by.username', 
        read_only=True,
        allow_null=True
    )
    updated_by_full_name: serializers.SerializerMethodField = serializers.SerializerMethodField()
    
    class Meta:
        model = PatientTransportReport
        fields = [
            'id',
            'patient',
            'attending_staff',
            'informed_consent',
            'care_transfer_report',
            'satisfaction_survey',
            'status',
            'created_at',
            'updated_at',
            'created_by',
            'created_by_username',
            'created_by_full_name',
            'updated_by',
            'updated_by_username',
            'updated_by_full_name'
        ]
        read_only_fields = fields
    
    def get_created_by_full_name(
        self, 
        obj: PatientTransportReport
    ) -> str | None:
        '''Get full name of creator.'''
        if not obj.created_by:
            return None
        return f'{obj.created_by.first_name} {obj.created_by.last_name}'.strip() or obj.created_by.username
    
    def get_updated_by_full_name(
        self, 
        obj: PatientTransportReport
    ) -> str | None:
        '''Get full name of last updater.'''
        if not obj.updated_by:
            return None
        return f'{obj.updated_by.first_name} {obj.updated_by.last_name}'.strip() or obj.updated_by.username