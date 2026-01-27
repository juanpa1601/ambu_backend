from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseView
from daily_monthly_inventory.application_service.list_shifts_application_service import (
    ListShiftsApplicationService,
)


class ListShiftsView(BaseView):
    """
    View for listing all available shifts (day/night).

    GET /api/daily-monthly-inventory/shifts/
    Returns a list of available shifts for dropdown selection.
    """

    def get(self, request: Request) -> Response:
        """
        Handle GET request to retrieve all shifts.

        Args:
            request: HTTP request

        Returns:
            Response with list of shifts or error
        """
        try:
            list_shifts_service: ListShiftsApplicationService = (
                ListShiftsApplicationService()
            )
            result: dict = list_shifts_service.list_shifts()

            return Response(
                result,
                status=result["status_code_http"],
            )

        except Exception:
            return Response(
                {
                    "response": "Ocurrió un error al listar las jornadas.",
                    "msg": -1,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
