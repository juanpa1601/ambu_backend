from typing import TypedDict
from datetime import datetime
from .companion_data import CompanionData
from .entity_data import EntityData

# ==================== INFORMED CONSENT ====================
class InformedConsentData(TypedDict, total=False):
    consent_timestamp: datetime 
    guardian_type: str
    guardian_name: str
    responsible_for: str
    guardian_id_type: str
    guardian_id_number: str
    # procedure: int
    administers_medications: bool
    # medication_administration: int
    service_type: str
    other_implications: str
    patient_can_sign: bool
    patient_signature: str
    responsible_can_sign: bool
    responsible_signature: str
    responsible: CompanionData
    attending_staff: int  # FK - OBLIGATORIO
    attending_staff_signature: str
    outgoing_entity: EntityData
    outgoing_entity_signature: str