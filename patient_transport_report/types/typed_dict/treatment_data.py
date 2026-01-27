from typing import TypedDict

# ==================== TREATMENT ====================
class TreatmentData(TypedDict, total=False):
    monitors_vital_signs: bool
    oxygen: bool
    liter_minute: float
    nasal_cannula: bool
    simple_face_mask: bool
    non_rebreather_mask: bool