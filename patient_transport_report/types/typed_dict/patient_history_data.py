from typing import TypedDict

# ==================== PATIENT HISTORY ====================
class PatientHistoryData(TypedDict, total=False):
    has_pathology: bool
    pathology: str
    has_allergies: bool
    allergies: str
    has_surgies: bool
    surgies: str
    has_medicines: bool
    medicines: str
    tobacco_user: bool
    substance_use: bool
    alcohol_user: bool
    other_history: str