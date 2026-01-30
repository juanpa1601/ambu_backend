from typing import TypedDict

# ==================== RESPONSE ====================
class SaveReportResponseData(TypedDict):
    report_id: int
    status: str
    completion_percentage: int
    can_complete: bool
    has_patient_info: bool
    has_informed_consent: bool
    has_care_transfer: bool
    has_satisfaction_survey: bool
    sections_updated: list[str]
    completed_at: str | None
    completed_by: str | None