from rest_framework import serializers
from patient_transport_report.models import RequiredProcedures

class RequiredProcedureDetailSerializer(serializers.ModelSerializer):
    '''Serializer for procedures performed.'''
    
    class Meta:
        model = RequiredProcedures
        fields = [
            'id',
            'immobilization',
            'stretcher_transfer',
            'ambulance_transport',
            'assessment',
            'other_procedure_details'
        ]
        read_only_fields = fields