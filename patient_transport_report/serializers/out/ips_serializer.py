from rest_framework import serializers
from patient_transport_report.models import IPS

class IPSSerializer(serializers.ModelSerializer):
    '''
    Serializer for IPS output (Receiving Institutions).
    
    Returns active IPS information.
    '''
    
    class Meta:
        model = IPS
        fields = [
            'id',
            'name',
            'is_active'
        ]
        read_only_fields = ['id']