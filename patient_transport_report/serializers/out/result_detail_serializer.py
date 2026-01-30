from rest_framework import serializers
from patient_transport_report.models import Result

class ResultDetailSerializer(serializers.ModelSerializer):
    '''Serializer for service result.'''
    
    class Meta:
        model = Result
        fields = [
            'id',
            'no_vital_signs',
            'denies_transportation',
            'schelud_transfer'
        ]
        read_only_fields = fields