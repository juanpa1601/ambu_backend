from rest_framework import serializers
from patient_transport_report.models import InformedConsent

class InformedConsentDetailSerializer(serializers.ModelSerializer):
    '''Serializer for InformedConsent details in report view.'''
    
    required_procedures_list: serializers.SerializerMethodField = serializers.SerializerMethodField()
    medication_administration_list: serializers.SerializerMethodField = serializers.SerializerMethodField()
    companion_name: serializers.CharField = serializers.CharField(source='companion.full_name', read_only=True)
    healthcare_staff_name: serializers.CharField = serializers.CharField(source='healthcare_staff.name', read_only=True)
    outgoing_entity_name: serializers.CharField = serializers.CharField(source='outgoing_entity.name', read_only=True)
    receiving_entity_name: serializers.CharField = serializers.CharField(source='receiving_entity.name', read_only=True)
    
    class Meta:
        model = InformedConsent
        fields = [
            'id',
            'required_procedures_list',
            'medication_administration_list',
            'companion',
            'companion_name',
            'healthcare_staff',
            'healthcare_staff_name',
            'outgoing_entity',
            'outgoing_entity_name',
            'receiving_entity',
            'receiving_entity_name',
            'signature'
        ]
        read_only_fields = fields
    
    def get_required_procedures_list(
        self, 
        obj: InformedConsent
    ) -> list[dict]:
        '''Get list of required procedures'''
        return list(obj.required_procedures.values('id', 'procedure_name'))
    
    def get_medication_administration_list(
        self, 
        obj: InformedConsent
    ) -> list[dict]:
        '''Get list of medication administrations'''
        return list(obj.medication_administration.values('id', 'medication_name', 'dose', 'route'))