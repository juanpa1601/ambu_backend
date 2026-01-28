from rest_framework import serializers
from patient_transport_report.models import Companion

class CompanionDetailSerializer(serializers.ModelSerializer):
    '''Serializer for companion/responsible person information.'''
    
    class Meta:
        model = Companion
        fields = [
            'id',
            'name',
            'identification_number',
            'kindship',
            'phone_number'
        ]
        read_only_fields = fields