from dataclasses import dataclass


@dataclass
class AmbulanceListItem:
    """DTO for ambulance list item."""

    id: int
    mobile_number: int
    license_plate: str
    display_name: str
