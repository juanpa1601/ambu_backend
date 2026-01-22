from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class InventoryDetailResponse:
    """Data Transfer Object for inventory detail response"""

    inventory_id: int
    system_user_id: int | None
    person_name: str
    date: date
    observations: str
    ambulance: dict[str, Any] | None
    biomedical_equipment: dict[str, Any] | None
    surgical: dict[str, Any] | None
    accessories_case: dict[str, Any] | None
    respiratory: dict[str, Any] | None
    immobilization_and_safety: dict[str, Any] | None
    accessories: dict[str, Any] | None
    additionals: dict[str, Any] | None
    pediatric: dict[str, Any] | None
    circulatory: dict[str, Any] | None
    ambulance_kit: dict[str, Any] | None
    created_at: str
