from rest_framework import serializers
from patient_transport_report.models import HemodynamicStatus

class HemodynamicStatusDetailSerializer(serializers.ModelSerializer):
    '''Serializer for hemodynamic status catalog.'''
    
    class Meta:
        model = HemodynamicStatus
        fields = [
            'id', 
            'name', 
            'order'
        ]
        read_only_fields = fields