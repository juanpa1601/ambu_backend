import logging

from daily_monthly_inventory.domain_service import InventoryDomainService
from daily_monthly_inventory.types.dataclass import ShiftListResponse


class ListShiftsApplicationService:
    """Application service for listing all available shifts."""

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.inventory_domain_service: InventoryDomainService = InventoryDomainService()

    def list_shifts(self) -> dict:
        """
        Retrieve all available shifts.

        Returns:
            Dictionary with shifts data and status
        """
        try:
            shift_response: ShiftListResponse = (
                self.inventory_domain_service.get_all_shifts()
            )

            # Convert dataclass to dict for JSON response
            shifts_list = [
                {"id": shift.id, "name": shift.name} for shift in shift_response.shifts
            ]

            return {
                "response": "Jornadas recuperadas exitosamente.",
                "msg": 1,
                "status_code_http": 200,
                "data": {
                    "shifts": shifts_list,
                    "total_count": shift_response.total_count,
                },
            }

        except Exception as e:
            self.logger.error(f"Error retrieving shifts: {str(e)}", exc_info=True)
            return {
                "response": "Ocurrió un error al recuperar las jornadas.",
                "msg": -1,
                "status_code_http": 500,
            }
