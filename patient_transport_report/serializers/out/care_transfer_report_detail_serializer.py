from rest_framework import serializers
from patient_transport_report.models import CareTransferReport

class CareTransferReportDetailSerializer(serializers.ModelSerializer):
    '''Serializer for CareTransferReport details in report view.'''
    
    driver_name: serializers.CharField = serializers.CharField(
        source='driver.name', 
        read_only=True
    )
    attending_staff_name: serializers.CharField = serializers.CharField(
        source='attending_staff.name', 
        read_only=True
    )
    support_staff_name: serializers.CharField = serializers.CharField(
        source='support_staff.name', 
        read_only=True
    )
    ambulance_plate: serializers.CharField = serializers.CharField(
        source='ambulance.plate_number', 
        read_only=True
    )
    companion_1_name: serializers.CharField = serializers.CharField(
        source='companion_1.full_name', 
        read_only=True
    )
    companion_2_name: serializers.CharField = serializers.CharField(
        source='companion_2.full_name', 
        read_only=True
    )
    receiving_entity_name: serializers.CharField = serializers.CharField(
        source='receiving_entity.name', 
        read_only=True
    )
    diagnosis_1_code: serializers.CharField = serializers.CharField(
        source='diagnosis_1.cie_10', 
        read_only=True
    )
    diagnosis_1_name: serializers.CharField = serializers.CharField(
        source='diagnosis_1.cie_10_name', 
        read_only=True
    )
    diagnosis_2_code: serializers.CharField = serializers.CharField(
        source='diagnosis_2.cie_10', 
        read_only=True
    )
    diagnosis_2_name: serializers.CharField = serializers.CharField(
        source='diagnosis_2.cie_10_name', 
        read_only=True
    )
    skin_conditions_list: serializers.SerializerMethodField = serializers.SerializerMethodField()
    hemodynamic_statuses_list: serializers.SerializerMethodField = serializers.SerializerMethodField()
    
    class Meta:
        model = CareTransferReport
        fields = [
            'id',
            'patient_one_of',
            'transfer_type',
            'initial_address',
            'landmark',
            'service_type',
            'dispatch_time',
            'patient_arrival_time',
            'patient_departure_time',
            'arrival_time_patient',
            'double_departure_time',
            'double_arrival_time',
            'end_attention_time',
            'driver',
            'driver_name',
            'attending_staff',
            'attending_staff_name',
            'reg_number',
            'support_staff',
            'support_staff_name',
            'attending_staff_tittle',
            'ambulance',
            'ambulance_plate',
            'companion_1',
            'companion_1_name',
            'companion_2',
            'companion_2_name',
            'initial_physicial_examination',
            'final_physical_examination',
            'skin_conditions_list',
            'hemodynamic_statuses_list',
            'treatment',
            'diagnosis_1',
            'diagnosis_1_code',
            'diagnosis_1_name',
            'diagnosis_2',
            'diagnosis_2_code',
            'diagnosis_2_name',
            'result',
            'complications_transfer',
            'notes',
            'receiving_entity',
            'receiving_entity_name'
        ]
        read_only_fields = fields
    
    def get_skin_conditions_list(
        self, 
        obj: CareTransferReport
    ) -> list[dict]:
        '''Get list of skin conditions'''
        return list(obj.skin_conditions.values('id', 'condition_name'))
    
    def get_hemodynamic_statuses_list(
        self, 
        obj: CareTransferReport
    ) -> list[dict]:
        '''Get list of hemodynamic statuses'''
        return list(obj.hemodynamic_statuses.values('id', 'status_name'))