from rest_framework import serializers

class ChangeUserStatusSerializer(serializers.Serializer):
    '''Serializer for changing user active status.'''
    status: serializers.BooleanField = serializers.BooleanField(
        required=True,
        help_text='New active status for the user (true/false)'
    )
    
    def validate_status(
        self, 
        value: bool
    ):
        '''Validate that status is a boolean.'''
        if not isinstance(value, bool):
            raise serializers.ValidationError('Status must be a boolean value.')
        return value