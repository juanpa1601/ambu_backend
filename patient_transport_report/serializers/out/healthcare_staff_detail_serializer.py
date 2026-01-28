from rest_framework import serializers
from staff.models import Healthcare

class HealthcareStaffDetailSerializer(serializers.ModelSerializer):
    '''Serializer for healthcare staff with base staff info.'''
    
    first_name: serializers.CharField = serializers.CharField(
        source='base_staff.first_name', 
        read_only=True
    )
    last_name: serializers.CharField = serializers.CharField(
        source='base_staff.last_name', 
        read_only=True
    )
    identification_number: serializers.CharField = serializers.CharField(
        source='base_staff.identification_number', 
        read_only=True
    )
    phone_number: serializers.CharField = serializers.CharField(
        source='base_staff.phone_number', 
        read_only=True
    )
    
    class Meta:
        model = Healthcare
        fields = [
            'base_staff_id',
            'first_name',
            'last_name',
            'identification_number',
            'phone_number',
            'professional_position',
            'professional_registration'
        ]
        read_only_fields = fields