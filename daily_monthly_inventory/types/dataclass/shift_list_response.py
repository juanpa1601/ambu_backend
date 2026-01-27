from dataclasses import dataclass

from .shift_list_item import ShiftListItem


@dataclass
class ShiftListResponse:
    """Response DTO for list of shifts"""

    shifts: list[ShiftListItem]
    total_count: int
