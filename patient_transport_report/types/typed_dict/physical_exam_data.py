from typing import TypedDict
from .glasgow_data import GlasgowData

# ==================== PHYSICAL EXAM ====================
class PhysicalExamData(TypedDict, total=False):
    systolic: float
    diastolic: float
    map_pam: float
    heart_rate: float
    respiratory_rate: float
    oxygen_saturation: float
    temperature: float
    blood_glucose: float
    glasgow: GlasgowData