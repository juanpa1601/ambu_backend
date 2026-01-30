from rest_framework import serializers
from patient_transport_report.models import OutgoingReceivingEntity

class OutgoingReceivingEntityDetailSerializer(serializers.ModelSerializer):
    '''Serializer for outgoing/receiving entity information.'''
    
    class Meta:
        model = OutgoingReceivingEntity
        fields = [
            'id',
            'name',
            'document',
            'staff_title'
        ]
        read_only_fields = fields