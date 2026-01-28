from rest_framework import serializers
from patient_transport_report.models import CareTransferReport
from .companion_detail_serializer import CompanionDetailSerializer
from .physical_exam_detail_serializer import PhysicalExamDetailSerializer
from .treatment_detail_serializer import TreatmentDetailSerializer
from .result_detail_serializer import ResultDetailSerializer
from .complications_transfer_detail_serializer import ComplicationsTransferDetailSerializer
from .outgoing_receiving_entity_detail_serializer import OutgoingReceivingEntityDetailSerializer
from .healthcare_staff_detail_serializer import HealthcareStaffDetailSerializer
from .driver_detail_serializer import DriverDetailSerializer
from .ambulance_detail_serializer import AmbulanceDetailSerializer
from .diagnosis_detail_serializer import DiagnosisDetailSerializer
from .ips_detail_serializer import IPSDetailSerializer
from .skin_condition_detail_serializer import SkinConditionDetailSerializer
from .hemodynamic_status_detail_serializer import HemodynamicStatusDetailSerializer

class CareTransferReportDetailSerializer(serializers.ModelSerializer):
    '''Complete serializer for CareTransferReport with all nested data.'''
    
    driver: DriverDetailSerializer = DriverDetailSerializer(read_only=True)
    attending_staff: HealthcareStaffDetailSerializer = HealthcareStaffDetailSerializer(read_only=True)
    ambulance: AmbulanceDetailSerializer = AmbulanceDetailSerializer(read_only=True)
    companion: CompanionDetailSerializer = CompanionDetailSerializer(read_only=True)
    responsible: CompanionDetailSerializer = CompanionDetailSerializer(read_only=True)
    initial_physical_exam: PhysicalExamDetailSerializer = PhysicalExamDetailSerializer(read_only=True)
    final_physical_exam: PhysicalExamDetailSerializer = PhysicalExamDetailSerializer(read_only=True)
    treatment: TreatmentDetailSerializer = TreatmentDetailSerializer(read_only=True)
    diagnosis_1: DiagnosisDetailSerializer = DiagnosisDetailSerializer(read_only=True)
    diagnosis_2: DiagnosisDetailSerializer = DiagnosisDetailSerializer(read_only=True)
    ips: IPSDetailSerializer = IPSDetailSerializer(read_only=True)
    result: ResultDetailSerializer = ResultDetailSerializer(read_only=True)
    complications_transfer: ComplicationsTransferDetailSerializer = ComplicationsTransferDetailSerializer(read_only=True)
    receiving_entity: OutgoingReceivingEntityDetailSerializer = OutgoingReceivingEntityDetailSerializer(read_only=True)
    
    skin_condition: SkinConditionDetailSerializer = SkinConditionDetailSerializer(
        source='skin_conditions', 
        many=True, 
        read_only=True
    )
    hemodynamic_status: HemodynamicStatusDetailSerializer = HemodynamicStatusDetailSerializer(
        source='hemodynamic_statuses', 
        many=True, 
        read_only=True
    )
    
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
            'attending_staff',
            'reg_number',
            'support_staff',
            'attending_staff_title',
            'ambulance',
            'companion',
            'companion_is_responsible',
            'responsible',
            'initial_physical_exam',
            'skin_condition',
            'hemodynamic_status',
            'treatment',
            'diagnosis_1',
            'diagnosis_2',
            'result',
            'ips',
            'complications_transfer',
            'notes',
            'final_physical_exam',
            'receiving_entity',
            'receiving_entity_signature',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields