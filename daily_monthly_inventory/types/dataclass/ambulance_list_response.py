from dataclasses import dataclass

from .ambulance_list_item import AmbulanceListItem


@dataclass
class AmbulanceListResponse:
    """Response DTO for ambulance list."""

    ambulances: list[AmbulanceListItem]
    total_count: int
