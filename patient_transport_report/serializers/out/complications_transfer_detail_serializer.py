from rest_framework import serializers
from patient_transport_report.models import ComplicationsTransfer

class ComplicationsTransferDetailSerializer(serializers.ModelSerializer):
    '''Serializer for complications during transfer.'''
    
    class Meta:
        model = ComplicationsTransfer
        fields = [
            'id',
            'description_complication',
            'register_code',
            'code',
            'record_waiting_time',
            'waiting_time',
            'time_code'
        ]
        read_only_fields = fields