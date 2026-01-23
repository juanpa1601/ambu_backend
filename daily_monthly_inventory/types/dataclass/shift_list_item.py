from dataclasses import dataclass


@dataclass
class ShiftListItem:
    """Data Transfer Object for shift list item"""

    id: int
    name: str
