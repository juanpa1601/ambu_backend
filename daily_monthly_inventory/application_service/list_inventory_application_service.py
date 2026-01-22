import logging
from typing import Any

from django.contrib.auth.models import User

from daily_monthly_inventory.domain_service import InventoryDomainService
from daily_monthly_inventory.types.dataclass import InventoryListResponse


class ListInventoryApplicationService:
    """
    Application service for listing inventories.
    Handles orchestration of inventory retrieval.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.inventory_domain_service: InventoryDomainService = InventoryDomainService()

    def list_inventories(self, requesting_user: User) -> dict[str, Any]:
        """
        List all daily/monthly inventories.

        Args:
            requesting_user: User making the request

        Returns:
            dictionary with response data and status
        """
        try:
            # Get all inventories
            inventory_response: InventoryListResponse = (
                self.inventory_domain_service.get_all_inventories()
            )
            inventory_items = inventory_response.inventories
            total_count = inventory_response.total_count

            # Build response
            inventories_data: list[dict[str, Any]] = [
                {
                    "inventory_id": item.inventory_id,
                    "person_name": item.person_name,
                    "mobile_number": item.mobile_number,
                    "date": item.date.isoformat() if item.date else None,
                }
                for item in inventory_items
            ]

            self.logger.info(
                f"User {requesting_user.username} successfully retrieved "
                f"{len(inventory_items)} inventories"
            )

            return {
                "response": "Inventarios recuperados exitosamente.",
                "msg": 1,
                "status_code_http": 200,
                "data": {"inventories": inventories_data, "total_count": total_count},
            }

        except Exception as e:
            self.logger.error(
                f"Error listing inventories for {requesting_user.username}: {str(e)}",
                exc_info=True,
            )
            return {
                "response": "Ocurrió un error al recuperar los inventarios.",
                "msg": -1,
                "status_code_http": 500,
            }
