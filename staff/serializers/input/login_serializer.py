from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    '''Serializer for user login validation'''
    username: serializers.CharField = serializers.CharField(
        max_length=150,
        required=True,
        help_text='Username for authentication'
    )
    password: serializers.CharField = serializers.CharField(
        max_length=128,
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        help_text='User password'
    )

    def validate_username(
        self, 
        value: str
    ) -> str:
        '''Validate and clean username'''
        return value.strip().lower()