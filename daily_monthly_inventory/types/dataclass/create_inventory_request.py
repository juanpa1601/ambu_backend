from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class CreateInventoryRequest:
    system_user_id: int
    date: date
    ambulance_id: int | None = None
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
    observations: str = ""
