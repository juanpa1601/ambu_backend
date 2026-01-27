from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class UpdateInventoryRequest:
    """DTO for updating an inventory."""

    inventory_id: int
    date: date | None = None
    observations: str | None = None
    ambulance_id: int | None = None
    shift_id: int | None = None
    support_staff: str | None = None
    biomedical_equipment: dict[str, Any] | None = None
    surgical: dict[str, Any] | None = None
    accessories_case: dict[str, Any] | None = None
    respiratory: dict[str, Any] | None = None
    immobilization_and_safety: dict[str, Any] | None = None
    accessories: dict[str, Any] | None = None
    additionals: dict[str, Any] | None = None
    pediatric: dict[str, Any] | None = None
    circulatory: dict[str, Any] | None = None
    ambulance_kit: dict[str, Any] | None = None
