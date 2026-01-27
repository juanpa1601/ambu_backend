from rest_framework import serializers

class CreateUserSerializer(serializers.Serializer):
    '''Serializer for creating a new user with staff profile.'''
    # System User fields (required)
    username: serializers.CharField = serializers.CharField(
        required=True,
        max_length=150,
        help_text='Username for authentication'
    )
    email: serializers.EmailField = serializers.EmailField(
        required=True,
        help_text='User email address'
    )
    password: serializers.CharField = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True,
        help_text='User password (minimum 8 characters)'
    )
    first_name: serializers.CharField = serializers.CharField(
        required=True,
        max_length=150,
        help_text='User first name'
    )
    last_name: serializers.CharField = serializers.CharField(
        required=True,
        max_length=150,
        help_text='User last name'
    )
    
    # Base Staff fields (required)
    document_type: serializers.ChoiceField = serializers.ChoiceField(
        required=True,
        choices=['DNI', 'CE', 'Passport', 'RUC', 'CC'],
        help_text='Type of identification document'
    )
    document_number: serializers.CharField = serializers.CharField(
        required=True,
        max_length=20,
        help_text='Document identification number'
    )
    type_personnel: serializers.ChoiceField = serializers.ChoiceField(
        required=True,
        choices=['Healthcare', 'Administrative', 'Driver'],
        help_text='Type of staff personnel'
    )
    phone_number: serializers.CharField = serializers.CharField(
        required=True,
        max_length=15,
        help_text='Contact phone number'
    )
    address: serializers.CharField = serializers.CharField(
        required=True,
        help_text='Physical address'
    )
    birth_date: serializers.DateField = serializers.DateField(
        required=True,
        help_text='Date of birth (YYYY-MM-DD)'
    )
    
    # Healthcare specific fields
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
    
    # Driver specific fields
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
    
    # Administrative specific fields
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
    
    def validate_type_personnel(
        self, 
        value: str
    ):
        '''Validate type_personnel is one of the allowed types'''
        if value not in ['Healthcare', 'Administrative', 'Driver']:
            raise serializers.ValidationError('Invalid personnel type.')
        return value
    
    def validate(
        self, 
        data: dict
    ):
        '''Validate that required fields for specific staff type are provided.'''
        type_personnel: str = data.get('type_personnel')
        # Validate Healthcare fields
        if type_personnel == 'Healthcare':
            if not data.get('professional_registration'):
                raise serializers.ValidationError({
                    'professional_registration': 'This field is required for Healthcare personnel.'
                })
            if not data.get('professional_position'):
                raise serializers.ValidationError({
                    'professional_position': 'This field is required for Healthcare personnel.'
                })
        # Validate Driver fields
        elif type_personnel == 'Driver':
            if not data.get('license_number'):
                raise serializers.ValidationError({
                    'license_number': 'This field is required for Driver personnel.'
                })
            if not data.get('license_category'):
                raise serializers.ValidationError({
                    'license_category': 'This field is required for Driver personnel.'
                })
        # Validate Administrative fields
        elif type_personnel == 'Administrative':
            if not data.get('department'):
                raise serializers.ValidationError({
                    'department': 'This field is required for Administrative personnel.'
                })
            if not data.get('role'):
                raise serializers.ValidationError({
                    'role': 'This field is required for Administrative personnel.'
                })
        return data