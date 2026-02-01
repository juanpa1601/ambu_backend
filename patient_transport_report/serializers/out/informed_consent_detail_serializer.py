from rest_framework import serializers
from patient_transport_report.models import InformedConsent
from .outgoing_receiving_entity_detail_serializer import OutgoingReceivingEntityDetailSerializer
from .required_procedure_detail_serializer import RequiredProcedureDetailSerializer
from .medication_administration_detail_serializer import MedicationAdministrationDetailSerializer

class InformedConsentDetailSerializer(serializers.ModelSerializer):
    '''Complete serializer for InformedConsent with all nested data.'''
    
    outgoing_entity: OutgoingReceivingEntityDetailSerializer = OutgoingReceivingEntityDetailSerializer(read_only=True)
    required_procedures: RequiredProcedureDetailSerializer = RequiredProcedureDetailSerializer(read_only=True)
    medication_administration: MedicationAdministrationDetailSerializer = MedicationAdministrationDetailSerializer(read_only=True)
    
    class Meta:
        model = InformedConsent
        fields = [
            'id',
            'consent_timestamp',
            'guardian_type',
            'guardian_name',
            'responsible_for',
            'guardian_id_type',
            'guardian_id_number',
            'required_procedures',
            'administers_medications',
            'medication_administration',
            'service_type',
            'other_implications',
            'patient_can_sign',
            'patient_signature',
            'responsible_can_sign',
            'responsible_signature',
            'attending_staff_signature',
            'outgoing_entity',
            'outgoing_entity_signature',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields