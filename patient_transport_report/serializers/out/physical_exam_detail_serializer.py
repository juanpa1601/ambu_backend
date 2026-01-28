from rest_framework import serializers
from patient_transport_report.models import PhysicalExam
from .glasgow_detail_serializer import GlasgowDetailSerializer

class PhysicalExamDetailSerializer(serializers.ModelSerializer):
    '''Serializer for physical examination with Glasgow scale.'''
    
    glasgow: GlasgowDetailSerializer = GlasgowDetailSerializer(read_only=True)
    
    class Meta:
        model = PhysicalExam
        fields = [
            'id',
            'systolic',
            'diastolic',
            'map_pam',
            'heart_rate',
            'respiratory_rate',
            'oxygen_saturation',
            'temperature',
            'blood_glucose',
            'glasgow'
        ]
        read_only_fields = fields