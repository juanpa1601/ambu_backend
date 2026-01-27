from typing import TypedDict
from datetime import datetime
from .companion_data import CompanionData
from .physical_exam_data import PhysicalExamData
from .treatment_data import TreatmentData
from .result_data import ResultData
from .complications_transfer_data import ComplicationsTransferData
from .entity_data import EntityData

# ==================== CARE TRANSFER REPORT ====================
class CareTransferReportData(TypedDict, total=False):
    patient_one_of: int
    transfer_type: str
    initial_address: str
    landmark: str
    service_type: str
    dispatch_time: str
    patient_arrival_time: str
    patient_departure_time: str
    arrival_time_patient: str
    double_departure_time: str
    double_arrival_time: str
    end_attention_time: str
    driver: int
    attending_staff: int
    reg_number: str
    support_staff: int
    attending_staff_title: str
    ambulance: int
    companion: CompanionData
    companion_is_responsible: bool
    responsible: CompanionData
    initial_physical_examination: PhysicalExamData
    final_physical_examination: PhysicalExamData
    skin_condition: list[int]
    hemodynamic_stats: list[int]
    treatment: TreatmentData
    diagnosis_1: int
    diagnosis_2: int
    result: ResultData
    ips: int
    complications_transfer: ComplicationsTransferData
    notes: str
    receiving_entity: EntityData
    receiving_entity_signature: str