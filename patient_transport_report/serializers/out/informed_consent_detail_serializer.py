from rest_framework import serializers
from patient_transport_report.models import InformedConsent
from .companion_detail_serializer import CompanionDetailSerializer
from .outgoing_receiving_entity_detail_serializer import OutgoingReceivingEntityDetailSerializer
from .required_procedure_detail_serializer import RequiredProcedureDetailSerializer
from .medication_administration_detail_serializer import MedicationAdministrationDetailSerializer
from .healthcare_staff_detail_serializer import HealthcareStaffDetailSerializer

class InformedConsentDetailSerializer(serializers.ModelSerializer):
    '''Complete serializer for InformedConsent with all nested data.'''
    
    responsible: CompanionDetailSerializer = CompanionDetailSerializer(read_only=True)
    attending_staff: HealthcareStaffDetailSerializer = HealthcareStaffDetailSerializer(read_only=True)
    outgoing_entity: OutgoingReceivingEntityDetailSerializer = OutgoingReceivingEntityDetailSerializer(read_only=True)
    required_procedure: RequiredProcedureDetailSerializer = RequiredProcedureDetailSerializer(read_only=True)
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
            'required_procedure',
            'administers_medications',
            'medication_administration',
            'service_type',
            'other_implications',
            'patient_can_sign',
            'patient_signature',
            'responsible_can_sign',
            'responsible_signature',
            'responsible',
            'attending_staff',
            'attending_staff_signature',
            'outgoing_entity',
            'outgoing_entity_signature',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields