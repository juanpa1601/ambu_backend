from rest_framework import serializers
from .patient_history_input_serializer import PatientHistoryInputSerializer
from .insurance_provider_input_serializer import InsuranceProviderInputSerializer

class PatientInputSerializer(serializers.Serializer):
    '''Input serializer for Patient data'''
    patient_name: serializers.CharField = serializers.CharField(
        max_length=200, 
        required=True
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
        required=False, 
        allow_blank=True
    )
    identification_number: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=True
    )
    issue_date: serializers.DateField = serializers.DateField(
        required=False, 
        allow_null=True
    )
    issue_place: serializers.CharField = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    birth_date: serializers.DateField = serializers.DateField(
        required=False, 
        allow_null=True
    )
    sex: serializers.CharField = serializers.CharField(
        max_length=10, 
        required=False, 
        allow_blank=True
    )
    home_address: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    residence_city: serializers.CharField = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )    
    cell_phone: serializers.CharField = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True
    )
    landline_phone: serializers.CharField = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True
    )
    marital_status: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    occupation: serializers.CharField = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    patient_history = PatientHistoryInputSerializer(
        required=False, 
        allow_null=True
    )
    insurance_provider = InsuranceProviderInputSerializer(
        required=False, 
        allow_null=True
    )
    membership_category: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
