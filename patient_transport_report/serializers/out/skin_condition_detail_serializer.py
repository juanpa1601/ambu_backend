from rest_framework import serializers
from patient_transport_report.models import SkinCondition

class SkinConditionDetailSerializer(serializers.ModelSerializer):
    '''Serializer for skin condition catalog.'''
    
    class Meta:
        model = SkinCondition
        fields = [
            'id', 
            'name', 
            'order'
        ]
        read_only_fields = fields