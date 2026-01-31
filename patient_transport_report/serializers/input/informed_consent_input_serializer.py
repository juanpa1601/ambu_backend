from rest_framework import serializers
from .companion_input_serializer import CompanionInputSerializer
from .entity_input_serializer import EntityInputSerializer
from .medication_administration_input_serializer import MedicationAdministrationInputSerializer
from .required_procedures_input_serializer import RequiredProceduresInputSerializer

# ==================== INFORMED CONSENT ====================
class InformedConsentInputSerializer(serializers.Serializer):
    consent_timestamp = serializers.DateTimeField(
        required=False,
        allow_null=True
    )
    guardian_type = serializers.ChoiceField(
        required=False,
        allow_null=True,
        allow_blank=True,
        choices=['paciente', 'acompañante', 'familiar'],
        help_text='Type of guardian'
    )
    guardian_name = serializers.CharField(
        max_length=200, 
        required=False, 
        allow_blank=True
    )
    responsible_for = serializers.CharField(
        max_length=200, 
        required=False, 
        allow_blank=True
    )
    guardian_id_type = serializers.ChoiceField(
        required=False,
        allow_null=True,
        allow_blank=True,
        choices=['cédula de ciudadanía', 
                 'tarjeta de identidad', 
                 'registro civil', 
                 'cédula de extranjería', 
                 'pasaporte', 
                 'dni/carné de identidad',
                 'permiso de protección temporal',
                 'documento de identidad extranjero'
                ],
        help_text='Type of identification document of the guardian'
    )
    guardian_id_number = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    procedure = RequiredProceduresInputSerializer(
        required=False, 
        allow_null=True
    )
    administers_medications = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    medication_administration = MedicationAdministrationInputSerializer(
        required=False, 
        allow_null=True
    )
    service_type = serializers.ChoiceField(
        required=False,
        allow_null=True,
        allow_blank=True,
        choices=['traslado asistencial de baja complejidad', 
                 'atención prehospitalaria doble'],
        help_text='Type of service provided'
    )
    other_implications = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    patient_can_sign = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    patient_signature = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    responsible_can_sign = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    responsible_signature = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    attending_staff_signature = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    outgoing_entity = EntityInputSerializer(
        required=False, 
        allow_null=True
    )
    outgoing_entity_signature = serializers.CharField(
        required=False, 
        allow_null=True,
        allow_blank=True
    )