from typing import TypedDict

# ==================== REQUIRED PROCEDURES ====================
class RequiredProceduresData(TypedDict, total=False):
    immobilization: bool
    stretcher_transfer: bool
    ambulance_transport: bool
    assessment: bool
    other_procedure_details: str