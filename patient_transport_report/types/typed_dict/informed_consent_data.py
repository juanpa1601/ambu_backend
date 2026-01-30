from typing import TypedDict
from datetime import datetime

from patient_transport_report.types.typed_dict.medication_administration_data import MedicationAdministrationData
from patient_transport_report.types.typed_dict.required_procedures_data import RequiredProceduresData
from .companion_data import CompanionData
from .entity_data import EntityData

# ==================== INFORMED CONSENT ====================
class InformedConsentData(TypedDict, total=False):
    consent_timestamp: str
    guardian_type: str
    guardian_name: str
    responsible_for: str
    guardian_id_type: str
    guardian_id_number: str
    procedure: RequiredProceduresData
    administers_medications: bool
    medication_administration: MedicationAdministrationData
    service_type: str
    other_implications: str
    patient_can_sign: bool
    patient_signature: str
    responsible_can_sign: bool
    responsible_signature: str
    attending_staff_signature: str
    outgoing_entity: EntityData
    outgoing_entity_signature: str