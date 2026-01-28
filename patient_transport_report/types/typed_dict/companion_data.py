from typing import TypedDict

# ==================== COMPANION ====================
class CompanionData(TypedDict, total=False):
    name: str
    identification_number: str
    phone_number: str
    kindship: str