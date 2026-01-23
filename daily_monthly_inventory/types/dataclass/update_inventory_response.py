from dataclasses import dataclass


@dataclass
class UpdateInventoryResponse:
    """DTO for update inventory response."""

    inventory_id: int
    date: str
    observations: str
    fields_updated: list[str]
