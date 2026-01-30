from rest_framework import serializers
from patient_transport_report.models import Diagnosis

class DiagnosisDetailSerializer(serializers.ModelSerializer):
    '''Serializer for diagnosis (CIE-10).'''
    
    class Meta:
        model = Diagnosis
        fields = [
            'id',
            'cie_10',
            'cie_10_name'
        ]
        read_only_fields = fields