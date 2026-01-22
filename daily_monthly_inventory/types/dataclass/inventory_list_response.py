from dataclasses import dataclass

from .inventory_list_item import InventoryListItem


@dataclass
class InventoryListResponse:
    """Data Transfer Object for inventory list response"""

    inventories: list[InventoryListItem]
    total_count: int
