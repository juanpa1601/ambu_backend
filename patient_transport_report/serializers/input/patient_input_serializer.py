from rest_framework import serializers
from .patient_history_input_serializer import PatientHistoryInputSerializer
from .insurance_provider_input_serializer import InsuranceProviderInputSerializer

class PatientInputSerializer(serializers.Serializer):
    '''Input serializer for Patient data'''
    patient_name: serializers.CharField = serializers.CharField(
        max_length=200,
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    identification_type: serializers.ChoiceField = serializers.ChoiceField(
        required=False,
        allow_null=True,
        allow_blank=True,
        choices=['cédula de ciudadanía', 
                 'tarjeta de identidad', 
                 'registro civil', 
                 'cédula de extranjería', 
                 'pasaporte', 
                 'permiso de protección temporal',
                 'otro'
                ],
        help_text='Type of identification document of the patient'
    )
    other_identification_type: serializers.CharField = serializers.CharField(
        max_length=100,
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    identification_number: serializers.CharField = serializers.CharField(
        max_length=50, 
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    issue_date: serializers.DateField = serializers.DateField(
        required=False, 
        allow_null=True
    )
    issue_place: serializers.CharField = serializers.CharField(
        max_length=100, 
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    birth_date: serializers.DateField = serializers.DateField(
        allow_null=True, 
        required=False
    )
    sex: serializers.CharField = serializers.CharField(
        max_length=10, 
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    home_address: serializers.CharField = serializers.CharField(
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    residence_city: serializers.CharField = serializers.CharField(
        max_length=100,
        allow_null=True, 
        allow_blank=True, 
        required=False
    )    
    cell_phone: serializers.CharField = serializers.CharField(
        max_length=20, 
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    landline_phone: serializers.CharField = serializers.CharField(
        max_length=20, 
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    marital_status: serializers.CharField = serializers.CharField(
        max_length=50, 
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    occupation: serializers.CharField = serializers.CharField(
        max_length=100, 
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
    patient_history = PatientHistoryInputSerializer(
        allow_null=True, 
        required=False
    )
    insurance_provider = InsuranceProviderInputSerializer(
        allow_null=True, 
        required=False
    )
    membership_category: serializers.CharField = serializers.CharField(
        max_length=50, 
        allow_null=True, 
        allow_blank=True, 
        required=False
    )
