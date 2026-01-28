from rest_framework import serializers
from patient_transport_report.models import InsuranceProvider

class InsuranceProviderDetailSerializer(serializers.ModelSerializer):
    '''Serializer for insurance provider information.'''
    
    class Meta:
        model = InsuranceProvider
        fields = [
            'id',
            'coverage_type',
            'provider_name',
            'other_coverage_type',
            'other_coverage_details'
        ]
        read_only_fields = fields