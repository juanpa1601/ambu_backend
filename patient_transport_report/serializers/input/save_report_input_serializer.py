from rest_framework import serializers
from .patient_input_serializer import PatientInputSerializer
from .informed_consent_input_serializer import InformedConsentInputSerializer
from .care_transfer_report_input_serializer import CareTransferReportInputSerializer
from .satisfaction_survey_input_serializer import SatisfactionSurveyInputSerializer
from staff.models import Healthcare

class SaveReportInputSerializer(serializers.Serializer):
    '''
    Main input serializer for SaveReportView.
    
    Fields:
    - report_id: Optional, for UPDATE mode
    - attending_staff: Required, ID of Healthcare staff (at root level)
    - patient: Optional, patient data
    - informed_consent: Optional, informed consent data
    - care_transfer_report: Optional, care transfer report data
    - satisfaction_survey: Optional, satisfaction survey data
    '''
    
    report_id: serializers.IntegerField = serializers.IntegerField(
        required=False, 
        allow_null=True,
        help_text='ID of existing report for UPDATE mode'
    )
    attending_staff: serializers.IntegerField = serializers.IntegerField(
        required=True,
        help_text='ID of Healthcare staff (base_staff_id)'
    )
    patient: PatientInputSerializer = PatientInputSerializer(
        required=False, 
        allow_null=True,
        help_text='Patient data (required for CREATE mode)'
    )
    informed_consent: InformedConsentInputSerializer = InformedConsentInputSerializer(
        required=False, 
        allow_null=True,
        help_text='Informed consent data'
    )
    care_transfer_report: CareTransferReportInputSerializer = CareTransferReportInputSerializer(
        required=False, 
        allow_null=True,
        help_text='Care transfer report data'
    )
    satisfaction_survey: SatisfactionSurveyInputSerializer = SatisfactionSurveyInputSerializer(
        required=False, 
        allow_null=True,
        help_text='Satisfaction survey data'
    )
    
    def validate_attending_staff(
        self, 
        value: int
    ) -> int:
        '''
        Validate that attending_staff ID exists in Healthcare table.
        
        Args:
            value: Healthcare base_staff_id
        
        Returns:
            int: Validated ID
        
        Raises:
            ValidationError: If Healthcare staff not found
        '''
        
        if not Healthcare.objects.filter(base_staff_id=value).exists():
            raise serializers.ValidationError(
                f'Personal de salud con ID {value} no encontrado.'
            )
        return value
    
    def validate(
        self, 
        data: dict
    ) -> dict:
        '''
        Cross-field validation.
        
        Rules:
        - CREATE mode (report_id is None):
            - patient data is required
            - attending_staff is required (already validated above)
        
        - UPDATE mode (report_id exists):
            - attending_staff is always required (already validated above)
            - patient, informed_consent, care_transfer_report, satisfaction_survey are optional
        
        Args:
            data: Validated field data
        
        Returns:
            dict: Validated data
        
        Raises:
            ValidationError: If validation fails
        '''
        report_id: int | None = data.get('report_id')
        patient: dict | None = data.get('patient')
        if report_id is None:
            if not patient:
                raise serializers.ValidationError({
                    'patient': 'Los datos del paciente son obligatorios al crear un nuevo reporte.'
                })
        return data