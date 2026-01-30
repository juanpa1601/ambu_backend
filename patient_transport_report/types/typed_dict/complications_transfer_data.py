from typing import TypedDict

# ==================== COMPLICATIONS ====================
class ComplicationsTransferData(TypedDict, total=False):
    description_complication: str
    register_code: bool
    code: str
    record_waiting_time: bool
    waiting_time: str # <--- TODO STR, INT o DATETIME
    time_code: str