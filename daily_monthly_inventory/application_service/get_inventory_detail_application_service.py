import logging
from typing import Any

from django.contrib.auth.models import User

from daily_monthly_inventory.domain_service import InventoryDomainService
from daily_monthly_inventory.types.dataclass import InventoryDetailResponse


class GetInventoryDetailApplicationService:
    """Application service for retrieving inventory details."""

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.inventory_domain_service: InventoryDomainService = InventoryDomainService()

    def get_inventory_detail(
        self,
        requesting_user: User,
        inventory_id: int,
    ) -> dict[str, Any]:
        """
        Get detailed information for a specific inventory.

        Args:
            requesting_user: User making the request
            inventory_id: ID of the inventory to retrieve

        Returns:
            dictionary with response data and status
        """
        try:
            # Get inventory detail from domain service
            detail_response: InventoryDetailResponse | None = (
                self.inventory_domain_service.get_inventory_by_id(inventory_id)
            )

            if not detail_response:
                self.logger.warning(
                    f"User {requesting_user.username} requested non-existent inventory {inventory_id}"
                )
                return {
                    "response": "Inventario no encontrado.",
                    "msg": -1,
                    "status_code_http": 404,
                }

            # Build response data
            inventory_data: dict[str, Any] = {
                "inventory_id": detail_response.inventory_id,
                "system_user_id": detail_response.system_user_id,
                "person_name": detail_response.person_name,
                "date": detail_response.date.isoformat(),
                "observations": detail_response.observations,
                "ambulance": detail_response.ambulance,
                "biomedical_equipment": detail_response.biomedical_equipment,
                "surgical": detail_response.surgical,
                "accessories_case": detail_response.accessories_case,
                "respiratory": detail_response.respiratory,
                "immobilization_and_safety": detail_response.immobilization_and_safety,
                "accessories": detail_response.accessories,
                "additionals": detail_response.additionals,
                "pediatric": detail_response.pediatric,
                "circulatory": detail_response.circulatory,
                "ambulance_kit": detail_response.ambulance_kit,
                "created_at": detail_response.created_at,
            }

            self.logger.info(
                f"User {requesting_user.username} successfully retrieved inventory {inventory_id}"
            )

            return {
                "response": "Inventario recuperado exitosamente.",
                "msg": 1,
                "status_code_http": 200,
                "data": inventory_data,
            }

        except Exception as e:
            self.logger.error(
                f"Error retrieving inventory {inventory_id} for {requesting_user.username}: {str(e)}",
                exc_info=True,
            )
            return {
                "response": "Ocurrió un error al recuperar el inventario.",
                "msg": -1,
                "status_code_http": 500,
            }
