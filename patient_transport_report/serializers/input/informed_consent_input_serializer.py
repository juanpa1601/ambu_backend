from rest_framework import serializers
from .companion_input_serializer import CompanionInputSerializer
from .entity_input_serializer import EntityInputSerializer

class InformedConsentInputSerializer(serializers.Serializer):
    '''Input serializer for Informed Consent'''
    consent_timestamp: serializers.DateTimeField = serializers.DateTimeField(
        required=False, 
        allow_null=True
    )
    guardian_type: serializers.CharField = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    guardian_name: serializers.CharField = serializers.CharField(
        max_length=200, 
        required=False, 
        allow_blank=True
    )
    responsible_for: serializers.CharField = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True
    )
    guardian_id_type: serializers.CharField = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True
    )
    guardian_id_number: serializers.CharField = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True
    )
    administers_medications: serializers.BooleanField = serializers.BooleanField(required=False)
    service_type: serializers.CharField = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )
    other_implications: serializers.CharField = serializers.CharField(
        required=False,
        allow_blank=True
    )
    patient_can_sign: serializers.BooleanField = serializers.BooleanField(required=False)
    patient_signature: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    responsible_can_sign: serializers.BooleanField = serializers.BooleanField(required=False)
    responsible_signature: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    responsible: CompanionInputSerializer = CompanionInputSerializer(
        required=False, 
        allow_null=True
    )
    attending_staff: serializers.IntegerField = serializers.IntegerField(required=True)  # OBLIGATORIO
    attending_staff_signature: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    outgoing_entity: EntityInputSerializer = EntityInputSerializer(
        required=False, 
        allow_null=True
    )
    outgoing_entity_signature: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )