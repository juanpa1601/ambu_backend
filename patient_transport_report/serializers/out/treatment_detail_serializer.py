from rest_framework import serializers
from patient_transport_report.models import Treatment

class TreatmentDetailSerializer(serializers.ModelSerializer):
    '''Serializer for treatment details.'''
    
    class Meta:
        model = Treatment
        fields = [
            'id',
            'monitors_vital_signs',
            'oxygen',
            'liters_minute',
            'nasal_cannula',
            'simple_face_mask',
            'non_rebreather_mask'
        ]
        read_only_fields = fields