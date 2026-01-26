from rest_framework import serializers
from staff.models import Driver

class DriverSerializer(serializers.ModelSerializer):
    '''
    Serializer for Driver output.
    
    Returns driver information with basic details.
    '''
    
    full_name: serializers.CharField = serializers.CharField(
        source='name', 
        read_only=True
    )
    system_user_id: serializers.IntegerField = serializers.IntegerField(
        source='user.id', 
        read_only=True
    )
    username: serializers.CharField = serializers.CharField(
        source='user.username', 
        read_only=True
    )
    
    class Meta:
        model = Driver
        fields = [
            'id',
            'system_user_id',
            'username',
            'full_name',
            'document_type',
            'document_number',
            'is_active'
        ]
        read_only_fields = fields