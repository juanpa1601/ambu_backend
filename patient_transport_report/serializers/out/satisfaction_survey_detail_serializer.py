from rest_framework import serializers
from patient_transport_report.models import SatisfactionSurvey

class SatisfactionSurveyDetailSerializer(serializers.ModelSerializer):
    '''Serializer for SatisfactionSurvey details in report view.'''
    
    class Meta:
        model = SatisfactionSurvey
        fields = [
            'id',
            'rating',
            'comments',
            'created_at'
        ]
        read_only_fields = fields