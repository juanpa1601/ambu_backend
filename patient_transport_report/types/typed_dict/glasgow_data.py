from typing import TypedDict

# ==================== GLASGOW ====================
class GlasgowData(TypedDict, total=False):
    motor: int
    motor_text: str
    verbal: int
    verbal_text: str
    eyes_opening: int
    eyes_opening_text: str
    total: int