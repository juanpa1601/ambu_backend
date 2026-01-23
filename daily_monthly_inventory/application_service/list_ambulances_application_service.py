import logging
from typing import Any

from django.contrib.auth.models import User

from daily_monthly_inventory.domain_service import InventoryDomainService
from daily_monthly_inventory.types.dataclass import AmbulanceListResponse


class ListAmbulancesApplicationService:
    """
    Application service for listing ambulances.
    Orchestrates ambulance retrieval and formats HTTP responses.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.inventory_domain_service: InventoryDomainService = InventoryDomainService()

    def list_ambulances(
        self,
        requesting_user: User,
    ) -> dict[str, Any]:
        """
        List all active ambulances for dropdown selection.

        Args:
            requesting_user: User making the request

        Returns:
            dictionary with response data and status
        """
        try:
            ambulance_response: AmbulanceListResponse = (
                self.inventory_domain_service.get_all_ambulances()
            )

            # Convert dataclass to dict for JSON response
            ambulances_list: list[dict[str, Any]] = [
                {
                    "id": ambulance.id,
                    "mobile_number": ambulance.mobile_number,
                    "license_plate": ambulance.license_plate,
                    "display_name": ambulance.display_name,
                }
                for ambulance in ambulance_response.ambulances
            ]

            self.logger.info(
                f"User {requesting_user.username} successfully retrieved "
                f"{ambulance_response.total_count} ambulances"
            )

            return {
                "response": "Ambulancias recuperadas exitosamente.",
                "msg": 1,
                "status_code_http": 200,
                "data": {
                    "ambulances": ambulances_list,
                    "total_count": ambulance_response.total_count,
                },
            }

        except Exception as e:
            self.logger.error(
                f"Error listing ambulances for {requesting_user.username}: {str(e)}",
                exc_info=True,
            )
            return {
                "response": "Ocurrió un error al recuperar las ambulancias.",
                "msg": -1,
                "status_code_http": 500,
            }
