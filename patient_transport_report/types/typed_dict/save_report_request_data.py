from typing import TypedDict
from .patient_data import PatientData
from .informed_consent_data import InformedConsentData
from .care_transfer_report_data import CareTransferReportData
from .satisfaction_survey_data import SatisfactionSurveyData

# ==================== MAIN REQUEST ====================
class SaveReportRequestData(TypedDict, total=False):
    report_id: int | None
    patient_data: PatientData
    informed_consent: InformedConsentData
    care_transfer_report: CareTransferReportData
    satisfaction_survey: SatisfactionSurveyData
    change_status_to: str  # 'completado' o 'borrador'