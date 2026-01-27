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
    guardian_type = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
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
    guardian_id_type = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
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
        default=False
    )
    medication_administration = MedicationAdministrationInputSerializer(
        required=False, 
        allow_null=True
    )
    service_type = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    other_implications = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    patient_can_sign = serializers.BooleanField(
        required=False, 
        default=False
    )
    patient_signature = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    responsible_can_sign = serializers.BooleanField(
        required=False, 
        default=False
    )
    responsible_signature = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    responsible = CompanionInputSerializer(
        required=False, 
        allow_null=True
    )
    attending_staff = serializers.IntegerField(required=True)
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
        allow_blank=True
    )