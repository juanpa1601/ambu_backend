from typing import TypedDict

# ==================== INSURANCE PROVIDER ====================
class InsuranceProviderData(TypedDict, total=False):
    coverage_type: str
    provider_name: str
    other_coverage_type: bool
    other_coverage_details: str