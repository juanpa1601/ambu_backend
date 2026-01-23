import logging
from typing import Any

from django.contrib.auth.models import User

from daily_monthly_inventory.domain_service import InventoryDomainService
from daily_monthly_inventory.models import Ambulance, DailyMonthlyInventory
from daily_monthly_inventory.types.dataclass import (
    UpdateInventoryRequest,
    UpdateInventoryResponse,
)


class UpdateInventoryApplicationService:
    """
    Application service for updating inventory information.
    Handles orchestration and delegates domain logic to InventoryDomainService.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.inventory_domain_service: InventoryDomainService = InventoryDomainService()

    def update_inventory(
        self,
        inventory_id: int,
        update_data: dict[str, Any],
        requesting_user: User,
    ) -> dict[str, Any]:
        """
        Update inventory information.

        Args:
            inventory_id: ID of the inventory to update
            update_data: Dictionary with fields to update
            requesting_user: User making the request

        Returns:
            dictionary with response data and status
        """
        try:
            # Build request DTO
            request_dto: UpdateInventoryRequest = UpdateInventoryRequest(
                inventory_id=inventory_id,
                date=update_data.get("date"),
                observations=update_data.get("observations"),
                ambulance_id=update_data.get("ambulance_id"),
                biomedical_equipment=update_data.get("biomedical_equipment"),
                surgical=update_data.get("surgical"),
                accessories_case=update_data.get("accessories_case"),
                respiratory=update_data.get("respiratory"),
                immobilization_and_safety=update_data.get("immobilization_and_safety"),
                accessories=update_data.get("accessories"),
                additionals=update_data.get("additionals"),
                pediatric=update_data.get("pediatric"),
                circulatory=update_data.get("circulatory"),
                ambulance_kit=update_data.get("ambulance_kit"),
            )

            # Delegate to domain service
            response_dto: UpdateInventoryResponse = (
                self.inventory_domain_service.update_inventory(request_dto)
            )

            self.logger.info(
                f"User {requesting_user.username} successfully updated inventory {inventory_id}"
            )

            return {
                "response": "Inventario actualizado exitosamente.",
                "msg": 1,
                "status_code_http": 200,
                "data": {
                    "inventory_id": response_dto.inventory_id,
                    "date": response_dto.date,
                    "observations": response_dto.observations,
                    "fields_updated": response_dto.fields_updated,
                },
            }

        except DailyMonthlyInventory.DoesNotExist:
            self.logger.warning(
                f"User {requesting_user.username} attempted to update non-existent inventory {inventory_id}"
            )
            return {
                "response": f"Inventario con ID {inventory_id} no encontrado.",
                "msg": -1,
                "status_code_http": 404,
            }

        except Ambulance.DoesNotExist:
            self.logger.warning(
                f"Ambulance not found while updating inventory {inventory_id}"
            )
            return {
                "response": "Ambulancia especificada no encontrada.",
                "msg": -1,
                "status_code_http": 400,
            }

        except Exception as e:
            self.logger.error(
                f"Error updating inventory {inventory_id} for {requesting_user.username}: {str(e)}",
                exc_info=True,
            )
            return {
                "response": "Ocurrió un error al actualizar el inventario.",
                "msg": -1,
                "status_code_http": 500,
            }
