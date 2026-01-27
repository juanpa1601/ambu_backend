from rest_framework import serializers
from patient_transport_report.models import Diagnosis

class DiagnosisSerializer(serializers.ModelSerializer):
    '''
    Serializer for Diagnosis output (CIE-10 codes).
    
    Returns diagnosis information with CIE-10 code and description.
    '''
    
    class Meta:
        model = Diagnosis
        fields = [
            'id',
            'cie_10',
            'cie_10_name'
        ]
        read_only_fields = ['id']
    
    def to_representation(
        self, 
        instance: Diagnosis
    ) -> dict:
        '''
        Customize output format.
        '''
        representation: dict = super().to_representation(instance)
        # Optionally, combine code and name for display
        representation['display_name'] = f'{instance.cie_10} - {instance.cie_10_name}'
        return representation