from rest_framework import serializers
from staff.models import Driver

class DriverDetailSerializer(serializers.ModelSerializer):
    '''Serializer for driver with base staff info.'''
    
    first_name: str = serializers.CharField(source='base_staff.first_name', read_only=True)
    last_name: str = serializers.CharField(source='base_staff.last_name', read_only=True)
    identification_number: str = serializers.CharField(source='base_staff.identification_number', read_only=True)
    phone_number: str = serializers.CharField(source='base_staff.phone_number', read_only=True)
    
    class Meta:
        model = Driver
        fields = [
            'base_staff_id',
            'first_name',
            'last_name',
            'identification_number',
            'phone_number',
            'license_number',
            'license_category'
        ]
        read_only_fields = fields