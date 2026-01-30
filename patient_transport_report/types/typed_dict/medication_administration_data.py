from typing import TypedDict

# ==================== MEDICATION ADMINISTRATION ====================
class MedicationAdministrationData(TypedDict, total=False):
    oxygen: bool
    iv_fluids: bool
    admin_route_type: bool
    other_medication_details: str