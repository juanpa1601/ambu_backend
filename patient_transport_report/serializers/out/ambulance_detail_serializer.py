from rest_framework import serializers
from daily_monthly_inventory.models import Ambulance

class AmbulanceDetailSerializer(serializers.ModelSerializer):
    '''Serializer for ambulance details.'''
    
    class Meta:
        model = Ambulance
        fields = [
            'id',
            'mobile_number',
            'license_plate',
            'is_active'
        ]
        read_only_fields = fields