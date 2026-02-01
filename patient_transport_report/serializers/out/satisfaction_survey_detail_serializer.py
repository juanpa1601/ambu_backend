from rest_framework import serializers
from patient_transport_report.models import SatisfactionSurvey

class SatisfactionSurveyDetailSerializer(serializers.ModelSerializer):
    '''Complete serializer for satisfaction survey.'''
    
    class Meta:
        model = SatisfactionSurvey
        fields = [
            'id',
            'satisfaction_survey_conducted',
            'ambulance_request_ease',
            'phone_support_quality',
            'service_punctuality',
            'clear_info_provided',
            'staff_appearance',
            'ambulance_cleanliness',
            'driving_quality',
            'return_trip_timeliness',
            'safety_and_reassurance',
            'staff_empathy',
            'overall_satisfaction',
            'would_recommend',
            'comments',
            'respondent_can_sign',
            'respondent_name',
            'respondent_id_number',
            'respondent_email',
            'respondent_phone',
            'respondent_signature',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields