from rest_framework import serializers
from patient_transport_report.models import IPS

class IPSDetailSerializer(serializers.ModelSerializer):
    '''Serializer for IPS (health institution).'''
    
    class Meta:
        model = IPS
        fields = [
            'id',
            'name',
            'is_active'
        ]
        read_only_fields = fields