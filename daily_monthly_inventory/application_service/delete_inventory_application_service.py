import logging
from typing import Any

from django.contrib.auth.models import User

from daily_monthly_inventory.models import DailyMonthlyInventory


class DeleteInventoryApplicationService:
    """
    Application service for deleting inventory.
    Handles orchestration of inventory deletion operations.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    def delete_inventory(
        self,
        inventory_id: int,
        requesting_user: User,
    ) -> dict[str, Any]:
        """
        Delete inventory by ID.

        Args:
            inventory_id: ID of the inventory to delete
            requesting_user: User making the request

        Returns:
            dictionary with response data and status
        """
        try:
            # Step 1: Get the inventory
            try:
                inventory: DailyMonthlyInventory = DailyMonthlyInventory.objects.get(
                    id=inventory_id
                )
            except DailyMonthlyInventory.DoesNotExist:
                self.logger.warning(
                    f"User {requesting_user.username} attempted to delete non-existent inventory {inventory_id}"
                )
                return {
                    "response": f"Inventario con ID {inventory_id} no encontrado.",
                    "msg": -1,
                    "status_code_http": 404,
                }

            # Step 2: Soft-delete the inventory using AuditedModel method
            if inventory.is_deleted:
                # already deleted
                return {
                    "response": f"Inventario con ID {inventory_id} ya está eliminado.",
                    "msg": -1,
                    "status_code_http": 400,
                }

            # Use soft_delete method from AuditedModel (tracks deleted_by and deleted_at)
            inventory.soft_delete(user=requesting_user)

            # Step 3: Build response
            self.logger.info(
                f"User {requesting_user.username} successfully deleted inventory {inventory_id}"
            )

            return {
                "response": "Inventario eliminado exitosamente.",
                "msg": 1,
                "status_code_http": 200,
                "data": {"inventory_id": inventory_id, "deleted": True},
            }

        except Exception as e:
            self.logger.error(
                f"Error deleting inventory {inventory_id} for {requesting_user.username}: {str(e)}",
                exc_info=True,
            )
            return {
                "response": "Ocurrió un error al eliminar el inventario.",
                "msg": -1,
                "status_code_http": 500,
            }
