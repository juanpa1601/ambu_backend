from rest_framework import serializers
from staff.models import Driver

class DriverDetailSerializer(serializers.ModelSerializer):
    '''Serializer for driver with base staff info.'''
    
    document_number: str = serializers.CharField(
        source='base_staff.document_number', 
        read_only=True
    )
    phone_number: str = serializers.CharField(
        source='base_staff.phone_number', 
        read_only=True
    )
    full_name: serializers.CharField = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = [
            'base_staff_id',
            'full_name',
            'document_number',
            'phone_number',
            'license_number',
            'license_category'
        ]
        read_only_fields = fields

    def get_full_name(
        self, 
        obj: Driver
    ) -> str:
        user: object | None = getattr(obj.base_staff, 'system_user', None)
        first: str = getattr(user, 'first_name', '') if user else ''
        last: str = getattr(user, 'last_name', '') if user else ''
        return f'{first} {last}'.strip()