from typing import TypedDict

# ==================== RESULT ====================
class ResultData(TypedDict, total=False):
    no_vital_signs: bool
    denies_transportation: bool
    schelud_transfer: bool