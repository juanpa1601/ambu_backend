from rest_framework import serializers
from patient_transport_report.models import MedicationAdministration

class MedicationAdministrationDetailSerializer(serializers.ModelSerializer):
    '''Serializer for medication administration details.'''
    
    class Meta:
        model = MedicationAdministration
        fields = [
            'id',
            'oxygen',
            'iv_fluids',
            'admin_route_type',
            'other_medication_details'
        ]
        read_only_fields = fields