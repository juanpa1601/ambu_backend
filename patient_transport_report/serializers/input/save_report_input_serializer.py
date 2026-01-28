from rest_framework import serializers
from .patient_input_serializer import PatientInputSerializer
from .informed_consent_input_serializer import InformedConsentInputSerializer
from .care_transfer_report_input_serializer import CareTransferReportInputSerializer
from .satisfaction_survey_input_serializer import SatisfactionSurveyInputSerializer

class SaveReportInputSerializer(serializers.Serializer):
    '''Main input serializer for SaveReportView'''
    report_id: serializers.IntegerField = serializers.IntegerField(
        required=False, 
        allow_null=True
    )
    patient: PatientInputSerializer = PatientInputSerializer(
        required=False, 
        allow_null=True
    )
    informed_consent: InformedConsentInputSerializer = InformedConsentInputSerializer(
        required=False, 
        allow_null=True
    )
    care_transfer_report: CareTransferReportInputSerializer = CareTransferReportInputSerializer(
        required=False, 
        allow_null=True
    )
    satisfaction_survey: SatisfactionSurveyInputSerializer = SatisfactionSurveyInputSerializer(
        required=False, 
        allow_null=True
    )
    
    def validate(
        self, 
        data: dict
    ) -> dict:
        '''Cross-field validation'''
        report_id: int = data.get('report_id')
        patient: PatientInputSerializer = data.get('patient')
        care_transfer_report: CareTransferReportInputSerializer = data.get('care_transfer_report')
        # CREATE mode: require patient and attending_staff
        if report_id is None:
            if not patient:
                raise serializers.ValidationError({
                    'patient': 'Patient data is required when creating a new report'
                })
            if not care_transfer_report or 'attending_staff' not in care_transfer_report:
                raise serializers.ValidationError({
                    'care_transfer_report': 'attending_staff is required when creating a new report'
                })
        # UPDATE mode: if care_transfer_report sent, attending_staff is mandatory
        if report_id is not None and care_transfer_report:
            if 'attending_staff' not in care_transfer_report:
                raise serializers.ValidationError({
                    'care_transfer_report': 'attending_staff is required in care_transfer_report'
                })
        return data