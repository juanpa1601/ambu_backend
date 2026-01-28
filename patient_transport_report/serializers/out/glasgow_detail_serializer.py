from rest_framework import serializers
from patient_transport_report.models import Glasgow

class GlasgowDetailSerializer(serializers.ModelSerializer):
    '''Serializer for Glasgow Coma Scale.'''
    
    class Meta:
        model = Glasgow
        fields = [
            'id',
            'motor',
            'motor_text',
            'verbal',
            'verbal_text',
            'eyes_opening',
            'eyes_opening_text',
            'total'
        ]
        read_only_fields = fields