import logging
from typing import Any

from django.contrib.auth.models import User

from daily_monthly_inventory.domain_service import InventoryDomainService
from daily_monthly_inventory.types.dataclass import (
    InventoryListResponse,
    InventoryListItem,
)
from staff.models import Healthcare, Administrative


class ListInventoryApplicationService:
    """
    Application service for listing inventories.
    Handles orchestration of inventory retrieval.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.inventory_domain_service: InventoryDomainService = InventoryDomainService()

    def list_inventories(
        self,
        requesting_user: User,
        ambulance_id: int | None = None,
        month: int | None = None,
        day: int | None = None,
        year: int | None = None,
    ) -> dict[str, Any]:
        """
        List all daily/monthly inventories.

        Args:
            requesting_user: User making the request
            ambulance_id: Optional ambulance ID filter
            month: Optional month filter
            day: Optional day filter
            year: Optional year filter

        Returns:
            dictionary with response data and status
        """
        try:
            # Determine if user should see only their own inventories
            system_user_filter: int | None = None
            
            # Check if user is superuser or administrative (can see all inventories)
            is_superuser: bool = requesting_user.is_superuser
            is_administrative: bool = Administrative.objects.filter(
                base_staff__system_user=requesting_user
            ).exists()
            
            # If user is healthcare (not superuser or administrative), filter by their user ID
            if not is_superuser and not is_administrative:
                is_healthcare: bool = Healthcare.objects.filter(
                    base_staff__system_user=requesting_user
                ).exists()
                
                if is_healthcare:
                    system_user_filter = requesting_user.id
                    self.logger.info(
                        f"Healthcare user {requesting_user.username} - filtering inventories by user ID"
                    )
            else:
                self.logger.info(
                    f"User {requesting_user.username} has full access - showing all inventories"
                )
            
            # Get inventories with optional filters
            inventory_response: InventoryListResponse = (
                self.inventory_domain_service.get_all_inventories(
                    ambulance_id=ambulance_id,
                    month=month,
                    day=day,
                    year=year,
                    system_user_id=system_user_filter,
                )
            )
            inventory_items: list[InventoryListItem] = inventory_response.inventories
            total_count: int = inventory_response.total_count

            # Build response
            inventories_data: list[dict[str, Any]] = [
                {
                    "inventory_id": item.inventory_id,
                    "person_name": item.person_name,
                    "mobile_number": item.mobile_number,
                    "date": item.date.isoformat() if item.date else None,
                    "is_completed": item.is_completed,
                    "shift": item.shift,
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
