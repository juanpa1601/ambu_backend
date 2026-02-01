from rest_framework import serializers
from daily_monthly_inventory.models import Ambulance

class AmbulanceDetailSerializer(serializers.ModelSerializer):
    '''Serializer for ambulance details.'''

    display_name: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = Ambulance
        fields = [
            'id',
            'mobile_number',
            'license_plate',
            'is_active',
            'display_name'
        ]
        read_only_fields = fields

    def get_display_name(
        self, 
        obj: Ambulance
    ) -> str:
        return f'Móvil {obj.mobile_number} - {obj.license_plate}'