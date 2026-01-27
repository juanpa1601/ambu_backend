from typing import TypedDict
from datetime import datetime
from .patient_history_data import PatientHistoryData
from .insurence_provider_data import InsuranceProviderData

# ==================== PATIENT DATA ====================
class PatientData(TypedDict, total=False):
    patient_name: str
    identification_type: str
    other_identification_type: str
    identification_number: str
    issue_date: datetime
    issue_place: str
    patient_age: int
    birth_date: datetime
    sex: str
    home_address: str
    residence_city: str
    cell_phone: str
    landline_phone: str
    marital_status: str
    occupation: str
    patient_history: PatientHistoryData
    insurance_provider: InsuranceProviderData
    membership_category: str # Contributivo o Subsidiado