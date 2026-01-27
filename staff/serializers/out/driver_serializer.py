from rest_framework import serializers
from staff.models import Driver

class DriverSerializer(serializers.ModelSerializer):
    '''
    Serializer for Driver output.
    
    Returns driver information with basic details.
    '''
    
    full_name: serializers.CharField = serializers.SerializerMethodField()
    system_user_id: serializers.IntegerField = serializers.IntegerField(
        source='base_staff.system_user.id', 
        read_only=True
    )
    username: serializers.CharField = serializers.CharField(
        source='base_staff.system_user.username', 
        read_only=True
    )
    document_type: serializers.CharField = serializers.CharField(
        source='base_staff.document_type',
        read_only=True
    )
    document_number: serializers.CharField = serializers.CharField(
        source='base_staff.document_number',
        read_only=True
    )
    phone_number: serializers.CharField = serializers.CharField(
        source='base_staff.phone_number',
        read_only=True
    )
    
    class Meta:
        model = Driver
        fields = [
            'base_staff',
            'system_user_id',
            'username',
            'full_name',
            'document_type',
            'document_number',
            'phone_number',
            'license_number',
            'license_category',
            'blood_type'
        ]
        read_only_fields = fields
    
    def get_full_name(
        self, 
        obj: Driver
    ) -> str:
        '''Get driver's full name from system user'''
        return obj.base_staff.system_user.get_full_name()