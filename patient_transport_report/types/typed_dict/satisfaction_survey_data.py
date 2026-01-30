from typing import TypedDict

# ==================== SATISFACTION SURVEY ====================
class SatisfactionSurveyData(TypedDict, total=False):
    ambulance_request_ease: str
    phone_support_quality: str
    service_punctuality: str
    clear_info_provided: str
    staff_appearance: str
    ambulance_cleanliness: str
    driving_quality: str
    return_trip_timeliness: str
    safety_and_reassurance: str
    staff_empathy: str
    overall_satisfaction: str
    would_recommend: str
    comments: str
    respondent_can_sign: bool
    respondent_name: str
    respondent_id_number: str
    respondent_email: str
    respondent_phone: str
    respondent_signature: str