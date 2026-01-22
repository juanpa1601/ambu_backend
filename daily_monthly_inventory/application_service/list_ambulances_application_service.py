import logging
from typing import Any

from django.contrib.auth.models import User

from daily_monthly_inventory.models import Ambulance


class ListAmbulancesApplicationService:
    """
    Application service for listing ambulances.
    Handles orchestration of ambulance retrieval for dropdown menus.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    def list_ambulances(self, requesting_user: User) -> dict[str, Any]:
        """
        List all active ambulances for dropdown selection.

        Args:
            requesting_user: User making the request

        Returns:
            dictionary with response data and status
        """
        try:
            # Get all active ambulances
            ambulances: list[Ambulance] = list(
                Ambulance.objects.filter(is_active=True).order_by("mobile_number")
            )

            # Build response
            ambulances_data: list[dict[str, Any]] = [
                {
                    "id": ambulance.id,
                    "mobile_number": ambulance.mobile_number,
                    "license_plate": ambulance.license_plate,
                    "display_name": f"Móvil {ambulance.mobile_number} - {ambulance.license_plate}"
                    if ambulance.license_plate
                    else f"Móvil {ambulance.mobile_number}",
                }
                for ambulance in ambulances
            ]

            self.logger.info(
                f"User {requesting_user.username} successfully retrieved "
                f"{len(ambulances_data)} ambulances"
            )

            return {
                "response": "Ambulancias recuperadas exitosamente.",
                "msg": 1,
                "status_code_http": 200,
                "data": {
                    "ambulances": ambulances_data,
                    "total_count": len(ambulances_data),
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
