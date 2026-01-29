from rest_framework import serializers
from .companion_input_serializer import CompanionInputSerializer
from .entity_input_serializer import EntityInputSerializer
from .physical_exam_input_serializer import PhysicalExamInputSerializer
from .treatment_input_serializer import TreatmentInputSerializer
from .result_input_serializer import ResultInputSerializer
from .complications_input_serializer import ComplicationsInputSerializer

# ==================== CARE TRANSFER REPORT ====================
class CareTransferReportInputSerializer(serializers.Serializer):
    patient_one_of = serializers.IntegerField(
        required=False, 
        allow_null=True
    )
    transfer_type = serializers.ChoiceField(
        required=False,
        allow_null=True,
        allow_blank=True,
        choices=['traslado asistencial básico-sencillo', 'traslado asistencial básico-doble'],
        help_text='Type of transfer provided'
    )
    initial_address = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    landmark = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    service_type = serializers.ChoiceField(
        required=False,
        allow_null=True,
        allow_blank=True,
        choices=['remisión', 'alta hospitalaria', 'redondo'],
        help_text='Type of service provided'
    )
    dispatch_time = serializers.DateTimeField(
        required=False, 
        allow_null=True
    )
    patient_arrival_time = serializers.DateTimeField(
        required=False, 
        allow_null=True
    )
    patient_departure_time = serializers.DateTimeField(
        required=False, 
        allow_null=True
    )
    arrival_time_patient = serializers.DateTimeField(
        required=False, 
        allow_null=True
    )
    double_departure_time = serializers.DateTimeField(
        required=False, 
        allow_null=True
    )
    double_arrival_time = serializers.DateTimeField(
        required=False, 
        allow_null=True
    )
    end_attention_time = serializers.DateTimeField(
        required=False, 
        allow_null=True
    )
    driver = serializers.IntegerField(
        required=False, 
        allow_null=True
    )
    support_staff = serializers.CharField(
        max_length=200, 
        required=False, 
        allow_blank=True
    )
    ambulance = serializers.IntegerField(
        required=False, 
        allow_null=True
    )
    companion = CompanionInputSerializer(
        required=False, 
        allow_null=True
    )
    companion_is_responsible = serializers.BooleanField(
        required=False, 
        default=False
    )
    responsible = CompanionInputSerializer(
        required=False, 
        allow_null=True
    )
    initial_physical_exam = PhysicalExamInputSerializer(
        required=False, 
        allow_null=True
    )
    final_physical_exam = PhysicalExamInputSerializer(
        required=False, 
        allow_null=True
    )
    skin_condition = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
    hemodynamic_stats = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
    treatment = TreatmentInputSerializer(
        required=False, 
        allow_null=True
    )
    diagnosis_1 = serializers.IntegerField(
        required=False, 
        allow_null=True
    )
    diagnosis_2 = serializers.IntegerField(
        required=False, 
        allow_null=True
    )
    result = ResultInputSerializer(
        required=False, 
        allow_null=True
    )
    ips = serializers.IntegerField(
        required=False, 
        allow_null=True
    )
    complications_transfer = ComplicationsInputSerializer(
        required=False, 
        allow_null=True
    )
    notes = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    receiving_entity = EntityInputSerializer(
        required=False, 
        allow_null=True
    )
    receiving_entity_signature = serializers.CharField(
        required=False, 
        allow_blank=True
    )