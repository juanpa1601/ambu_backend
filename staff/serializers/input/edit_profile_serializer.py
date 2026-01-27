from rest_framework import serializers

class EditProfileSerializer(serializers.Serializer):
    '''
    Serializer for editing user's own profile.
    All fields are optional - only provided fields will be updated.
    '''
    # System User fields (optional)
    username: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=150,
        help_text='Unique username'
    )
    email: serializers.EmailField = serializers.EmailField(
        required=False,
        allow_null=True,
        help_text='User email address'
    )
    first_name: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=150,
        help_text='User first name'
    )
    last_name: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=150,
        help_text='User last name'
    )
    password: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        min_length=8,
        write_only=True,
        help_text='New password (minimum 8 characters)'
    )
    
    # Base Staff fields (optional)
    document_type: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=50,
        help_text='Type of identification document (DNI, Passport, etc.)'
    )
    document_number: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=50,
        help_text='Identification document number'
    )
    phone_number: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=15,
        help_text='Contact phone number'
    )
    address: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        help_text='Physical address'
    )
    birth_date: serializers.DateField = serializers.DateField(
        required=False,
        allow_null=True,
        help_text='Date of birth (YYYY-MM-DD)'
    )
    
    # Healthcare specific fields (optional)
    professional_registration: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=50,
        help_text='Professional registration number (CMP, etc.)'
    )
    professional_position: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=100,
        help_text='Professional position (Paramedic, Doctor, etc.)'
    )
    
    # Driver specific fields (optional)
    license_number: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=50,
        help_text='Driver license number'
    )
    license_category: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=10,
        help_text='License category (A-IIb, etc.)'
    )
    license_issue_date: serializers.DateField = serializers.DateField(
        required=False,
        allow_null=True,
        help_text='License issue date (YYYY-MM-DD)'
    )
    license_expiry_date: serializers.DateField = serializers.DateField(
        required=False,
        allow_null=True,
        help_text='License expiry date (YYYY-MM-DD)'
    )
    blood_type: serializers.ChoiceField = serializers.ChoiceField(
        required=False,
        allow_null=True,
        choices=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        help_text='Blood type'
    )
    
    # Administrative specific fields (optional)
    department: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=100,
        help_text='Department name'
    )
    role: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=100,
        help_text='Role or position'
    )
    access_level: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=50,
        help_text='Access level'
    )
    
    def validate(
        self, 
        data: dict
    ) -> dict:
        '''Validate that at least one field is provided for update.'''
        if not data:
            raise serializers.ValidationError('At least one field must be provided for update.')
        return data
    
    def validate_email(
        self, 
        value: str
    ) -> str:
        '''Validate email format'''
        if value and '@' not in value:
            raise serializers.ValidationError('Invalid email format.')
        return value