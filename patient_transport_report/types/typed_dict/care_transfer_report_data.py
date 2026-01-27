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
    dispatch_time: datetime
    patient_arrival_time: datetime
    patient_departure_time: datetime
    arrival_time_patient: datetime
    double_departure_time: datetime
    double_arrival_time: datetime
    end_attention_time: datetime
    driver: int  # FK
    attending_staff: int  # FK - OBLIGATORIO
    reg_number: str
    support_staff: str
    attending_staff_title: str
    ambulance: int  # FK
    companion: CompanionData
    companion_is_responsible: bool
    responsible: CompanionData
    initial_physical_examination: PhysicalExamData
    skin_conditions: list[int]  # M2M
    hemodynamic_statuses: list[int]  # M2M
    treatment: TreatmentData
    diagnosis_1: int  # FK
    diagnosis_2: int  # FK
    result: ResultData
    receiving_entity: EntityData
    complications_transfer: ComplicationsTransferData
    notes: str
    final_physical_examination: PhysicalExamData
    receiving_entity_signature: str
    ips: int  # FK