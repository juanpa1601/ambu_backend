from typing import TypedDict

# ==================== OUTGOING/RECEIVING ENTITY ====================
class EntityData(TypedDict, total=False):
    name: str
    document: str
    staff_title: str